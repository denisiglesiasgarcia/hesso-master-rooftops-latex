#!/usr/bin/env python3
"""Strip LaTeX constructs that pandoc's table reader can't parse, producing a
throwaway copy used only as pandoc's input. The original .tex sources are
never modified — convert_thesis.sh writes the result to a temp file.

Pandoc silently drops an entire \\begin{table} block (no warning, no AST
node) if its \\tabular is wrapped in \\makebox[\\textwidth][c]{...}, or if a
row uses \\multicolumn. Both are common in this thesis for centering wide
tables and for divider rows.
"""

import base64
import json
import re
import sys


def _read_balanced_group(text: str, start: int) -> tuple[str, int]:
    """text[start] must be '{'. Returns (inner_content, index_after_closing_brace)."""
    assert text[start] == "{"
    depth = 1
    j = start + 1
    while depth > 0 and j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
        j += 1
    return text[start + 1 : j - 1], j


def unwrap_makebox_centering(text: str) -> str:
    marker = r"\makebox[\textwidth][c]"
    out = []
    i = 0
    while True:
        idx = text.find(marker, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        brace_start = idx + len(marker)
        inner, after = _read_balanced_group(text, brace_start)
        out.append(inner)
        i = after
    return "".join(out)


def unwrap_makecell(text: str) -> str:
    """\\makecell[l]{Linknet +\\\\EfficientNet-B5} forces a two-line table cell
    in LaTeX. Pandoc's pipe-table writer can't represent a multi-line cell,
    so it silently drops everything up to the internal line break and turns
    the break itself into a spurious blank table row — every model name in
    this thesis's results tables loses its architecture half (only the
    encoder name like "EfficientNet-B5" survives) and gains a blank row
    after it. Unwrap the macro and join the two lines with a space instead."""
    marker = r"\makecell"
    out = []
    i = 0
    while True:
        idx = text.find(marker, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        j = idx + len(marker)
        if j < len(text) and text[j] == "[":
            _opt, j = _read_bracket_group(text, j)
        inner, after = _read_balanced_group(text, j)
        out.append(inner.replace("\\\\", " "))
        i = after
    return "".join(out)


def expand_multicolumn_dividers(text: str) -> str:
    """pandoc's table reader natively understands \\multicolumn/\\multirow
    fine when they describe a genuine spanning header or row label (it turns
    them into real colspan/rowspan) — but a row consisting of *only* one
    \\multicolumn spanning the full row width (used here purely as a
    full-width section-divider line, e.g. "Couverture"/"Stockage") makes it
    drop the entire table with no warning. Only flatten that specific
    divider-row case into plain text + padding cells; leave any row that
    mixes multicolumn/multirow with other real cells alone, since pandoc
    handles that correctly on its own and flattening it instead breaks the
    column alignment (e.g. turns a real 2-column header span into a single
    unspanned cell)."""
    marker = r"\multicolumn{"
    out = []
    i = 0
    while True:
        idx = text.find(marker, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        n_str, after_n = _read_balanced_group(text, idx + len(marker) - 1)
        _spec, after_spec = _read_balanced_group(text, after_n)
        content, after_content = _read_balanced_group(text, after_spec)

        row_start = text.rfind(r"\\", 0, idx) + 2
        row_end = text.find(r"\\", after_content)
        if row_end == -1:
            row_end = len(text)
        row = text[row_start:row_end]
        is_sole_spanner_on_row = row.count(r"\multicolumn{") + row.count(r"\multirow{") == 1

        if is_sole_spanner_on_row:
            n = int(n_str)
            out.append(content + " &" * (n - 1))
            i = after_content
        else:
            out.append(text[idx:after_content])
            i = after_content
    return "".join(out)


def strip_clines(text: str) -> str:
    """\\cline{3-4} draws a horizontal rule under only columns 3-4 (instead
    of the full row like \\hline). Pandoc's table reader doesn't know it and
    — instead of ignoring it like \\hline — treats it as literal cell
    content, leaking "3-4" as visible text into a cell and adding a whole
    spurious extra row for any \\cline that sits after the last data row."""
    return re.sub(r"\\cline\{[^}]*\}", "", text)


def strip_addlinespace(text: str) -> str:
    return text.replace(r"\addlinespace", "")


def fix_nameref_pageref(text: str) -> str:
    """\\nameref{X} (the target section's title) and \\pageref{X} (its PDF
    page number) come from the hyperref/nameref packages, which pandoc's
    LaTeX reader has never heard of — it silently drops both commands
    entirely, leaving a dangling, empty "(voir page )" parenthetical behind.
    A web page has no page numbers anyway: drop the page reference outright,
    and turn \\nameref into a plain \\ref, which the rest of this pipeline
    already resolves to a working link showing the section's real title."""
    text = re.sub(r"\s*\(voir\s+page~?\\pageref\{[^}]*\}\)", "", text)
    text = re.sub(r"\s*(?:à\s+la\s+)?page~?\\pageref\{[^}]*\}", "", text)
    return text.replace(r"\nameref{", r"\ref{")


def _find_command(text: str, command: str, start: int = 0):
    """Find `command{...}` (e.g. "\\caption{...}") anywhere at-or-after
    `start`, skipping false matches that are a prefix of a longer command
    name. Returns (arg_content, command_start_index, index_after_arg), or
    (None, None, start) if not found."""
    idx = start
    while True:
        idx = text.find(command, idx)
        if idx == -1:
            return None, None, start
        end_name = idx + len(command)
        if end_name < len(text) and text[end_name].isalpha():
            idx += 1
            continue
        if end_name >= len(text) or text[end_name] != "{":
            idx += 1
            continue
        content, after = _read_balanced_group(text, end_name)
        return content, idx, after


def _find_caption(block: str):
    """Handles both \\caption{text} and \\captionof{type}{text} (the latter
    is used inside this thesis's non-floating `code` environment)."""
    content, start, after = _find_command(block, r"\caption")
    if content is not None:
        return content, start, after
    _kind, start2, after_kind = _find_command(block, r"\captionof")
    if start2 is None:
        return None, None, 0
    j = after_kind
    while j < len(block) and block[j].isspace():
        j += 1
    if j < len(block) and block[j] == "{":
        text_content, after_text = _read_balanced_group(block, j)
        return text_content, start2, after_text
    return None, None, 0


def convert_code_listings(text: str) -> str:
    """This thesis defines custom `code`/`pythoncode`/`textcode` environments
    (via minted's \\newminted + \\newfloat) that pandoc's LaTeX reader has no
    knowledge of — it silently drops every \\begin{code}...\\end{code} block
    in its entirety. Rewrite each block into plain \\verbatim (which pandoc
    converts to a real fenced code block) plus a `[[CODEBLOCK:label:caption]]`
    sentinel paragraph that fix_text.py turns into a numbered caption with a
    working anchor."""
    begin_marker = r"\begin{code}"
    end_marker = r"\end{code}"
    out = []
    i = 0
    while True:
        idx = text.find(begin_marker, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        j = idx + len(begin_marker)
        if j < len(text) and text[j] == "[":
            j = text.find("]", j) + 1
        end_idx = text.find(end_marker, j)
        block = text[j:end_idx]

        caption, cap_start, after_caption = _find_caption(block)
        label, label_start, after_label = (None, None, None)
        if caption is not None:
            label, label_start, after_label = _find_command(block, r"\label", after_caption)
        if caption is not None:
            remove_start = cap_start
            remove_end = after_label if label is not None else after_caption
            block = block[:remove_start] + block[remove_end:]
        # Mark each sub-block's language so fix_text.py can turn the indented
        # code blocks pandoc produces from \verbatim into fenced, highlighted
        # ```python / ```text blocks (mkdocs has pymdownx.superfences for this).
        block = block.replace(r"\begin{pythoncode}", "§§CODESTART§§python§§\n\\begin{verbatim}")
        block = block.replace(r"\end{pythoncode}", r"\end{verbatim}" + "\n§§CODEEND§§")
        block = block.replace(r"\begin{textcode}", "§§CODESTART§§text§§\n\\begin{verbatim}")
        block = block.replace(r"\end{textcode}", r"\end{verbatim}" + "\n§§CODEEND§§")

        # "[" / "]" / "_" get backslash-escaped by pandoc's markdown writer;
        # avoid them in the sentinel so fix_text.py's regex matches reliably.
        sentinel = f"§§CODECAPTION§§{label or ''}§§{(caption or '').strip()}§§"
        out.append(f"{block}\n\n{sentinel}\n")
        i = end_idx + len(end_marker)
    return "".join(out)


def _read_bracket_group(text: str, start: int) -> tuple[str, int]:
    """text[start] must be '['. Returns (inner_content, index_after_closing_bracket)."""
    assert text[start] == "["
    depth = 1
    j = start + 1
    while depth > 0 and j < len(text):
        if text[j] == "[":
            depth += 1
        elif text[j] == "]":
            depth -= 1
        j += 1
    return text[start + 1 : j - 1], j


def _collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _parse_longtblr_body(body: str) -> dict:
    header_m = re.match(
        r"\s*\\textbf\{([^}]*)\}\s*&\s*\\textbf\{([^}]*)\}\s*&\s*\\textbf\{([^}]*)\}\s*\\\\",
        body,
    )
    header = list(header_m.groups()) if header_m else ["", "", ""]
    if header_m:
        body = body[header_m.end() :]

    row_re = re.compile(
        r"\\textbf\{(?P<name>[^}]*)\}.*?&\s*"
        r"\\begin\{itemize\}\[[^\]]*\](?P<col2>.*?)\\end\{itemize\}\s*&\s*"
        r"\\begin\{itemize\}\[[^\]]*\](?P<col3>.*?)\\end\{itemize\}\s*\\\\",
        re.DOTALL,
    )
    rows = []
    for m in row_re.finditer(body):
        items2 = [
            _collapse_ws(i)
            for i in re.findall(r"\\item\s+(.*?)(?=\\item|\Z)", m.group("col2"), re.DOTALL)
        ]
        items3 = [
            _collapse_ws(i)
            for i in re.findall(r"\\item\s+(.*?)(?=\\item|\Z)", m.group("col3"), re.DOTALL)
        ]
        rows.append([_collapse_ws(m.group("name")), items2, items3])
    return {"header": header, "rows": rows}


def convert_longtblr_tables(text: str) -> str:
    """The tabularray package's `longtblr` environment (used here for two
    wide comparison tables with bullet lists in each cell) is just as
    invisible to pandoc's LaTeX reader as \\begin{table} is when it can't
    parse the contents — the whole block is silently dropped. Pandoc can't
    represent multi-line/list cell content in a pipe table anyway, so encode
    the parsed rows as a base64 JSON payload in a sentinel; fix_text.py
    decodes it and emits a real HTML table. Inline \\citeyear/\\cite inside
    cells are dropped (citeproc never sees this extracted text)."""
    marker = r"\begin{longtblr}["
    out = []
    i = 0
    while True:
        idx = text.find(marker, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx])
        bracket_start = idx + len(marker) - 1
        opts, after_opts = _read_bracket_group(text, bracket_start)
        colspec_start = after_opts
        while text[colspec_start] != "{":
            colspec_start += 1
        _colspec, after_colspec = _read_balanced_group(text, colspec_start)
        end_idx = text.find(r"\end{longtblr}", after_colspec)
        body = text[after_colspec:end_idx]

        cap_m = re.search(r"caption\s*=\s*\{(.*?)\}\s*,", opts, re.DOTALL)
        label_m = re.search(r"label\s*=\s*\{(.*?)\}\s*,?", opts, re.DOTALL)
        caption_text = cap_m.group(1).strip() if cap_m else ""
        label_text = label_m.group(1).strip() if label_m else ""

        data = _parse_longtblr_body(body)
        payload = base64.b64encode(json.dumps(data, ensure_ascii=False).encode("utf-8")).decode(
            "ascii"
        )
        sentinel = f"§§RAWTABLE§§{label_text}§§{caption_text}§§{payload}§§"
        out.append(sentinel + "\n")
        i = end_idx + len(r"\end{longtblr}")
    return "".join(out)


def preprocess(text: str) -> str:
    text = unwrap_makebox_centering(text)
    text = unwrap_makecell(text)
    text = expand_multicolumn_dividers(text)
    text = strip_clines(text)
    text = strip_addlinespace(text)
    text = fix_nameref_pageref(text)
    text = convert_code_listings(text)
    text = convert_longtblr_tables(text)
    return text


def main() -> None:
    src_path, dst_path = sys.argv[1], sys.argv[2]
    with open(src_path, encoding="utf-8") as f:
        text = f.read()
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(preprocess(text))


if __name__ == "__main__":
    main()
