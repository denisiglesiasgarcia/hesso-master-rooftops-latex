#!/usr/bin/env python3
"""Post-process pandoc's generated Markdown:

1. Un-escape math pandoc mangles when it falls back to raw TeX (it runs the
   equation source through its markdown-escaping rules, e.g. `x_1` becomes
   the literal text `x\\_1`, breaking the subscript once MathJax renders it).
2. Expand the §§CODESTART/CODEEND§§, §§CODECAPTION§§ and §§RAWTABLE§§
   sentinels preprocess_tex.py left behind into real fenced code blocks, HTML
   tables, and numbered captions with working anchors.
3. Resolve figure/table/equation/section/chapter cross-references that
   pandoc leaves as raw "[label]" text because it never builds an anchor for
   them (this happens for any LaTeX construct it can't parse into its own
   AST — custom environments, multi-line math, or cross-chapter labels).

Run after fix_images.py, from the repo root.
"""

import base64
import html
import json
import re
from pathlib import Path

DOCS = Path("docs")


def fix_bare_url_autolinks(text: str) -> str:
    """Pandoc writes bare URLs (e.g. in the bibliography) as CommonMark
    autolinks `<https://...>`. python-markdown's HTML-block handling treats
    that as an unrecognized HTML tag and the browser silently discards it —
    the URL just vanishes. Rewrite to plain `[url](url)` link syntax, which
    renders correctly everywhere."""
    return re.sub(r"<(https?://[^\s<>]+)>", r"[\1](\1)", text)


def fix_bracket_escapes(text: str) -> str:
    """A markdown-escaped literal bracket (`\\[`, `\\]` — pandoc's way of
    writing a literal `[`/`]` that isn't link syntax, e.g. in a citation's
    numeric prefix, an interval like `[0.5:0.95]`, or a title containing
    brackets) reads as a backslash followed by a bracket all the way through
    to the rendered page. MathJax's `\\[...\\]` is also its display-math
    delimiter, so pymdownx.arithmatex grabs any such pair and renders it as a
    centered equation instead of text. Use the HTML entity instead so it can
    never collide with that — but only outside real `$$...$$` blocks, where
    `\\[`/`\\]` may be genuine interval notation MathJax needs verbatim."""
    parts = re.split(r"(\$\$.*?\$\$)", text, flags=re.DOTALL)
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace(r"\[", "&#91;").replace(r"\]", "&#93;")
    return "".join(parts)


def unescape_markdown(s: str) -> str:
    for esc, plain in [
        (r"\_", "_"),
        (r"\|", "|"),
        (r"\{", "{"),
        (r"\}", "}"),
        (r"\#", "#"),
        (r"\%", "%"),
        (r"\&", "&"),
        (r"\$", "$"),
    ]:
        s = s.replace(esc, plain)
    return s


def fix_math_escaping(text: str) -> str:
    def repl(m: re.Match) -> str:
        block = m.group(0).replace(r"\_", "_").replace(r"\|", "|")
        # \bm{...} is from LaTeX's `bm` package (bold vectors); MathJax's
        # default bundle has no idea what \bm is and renders it garbled
        # ("\bw" instead of bold w) since it isn't one of its own macros.
        # \boldsymbol is the MathJax/amsmath equivalent — same visual result.
        return block.replace(r"\bm{", r"\boldsymbol{")

    return re.sub(r"\$\$.*?\$\$", repl, text, flags=re.DOTALL)


def expand_code_blocks(text: str) -> str:
    def repl(m: re.Match) -> str:
        lang, raw = m.group(1), m.group(2)
        lines = raw.split("\n")
        dedented = []
        for line in lines:
            if line.startswith("    "):
                dedented.append(line[4:])
            elif line.strip() == "":
                dedented.append("")
            else:
                dedented.append(line.lstrip())
        code = "\n".join(dedented).strip("\n")
        return f"```{lang}\n{code}\n```"

    return re.sub(r"§§CODESTART§§(\w+)§§(.*?)§§CODEEND§§", repl, text, flags=re.DOTALL)


# Every `<p class="thesis-caption">` built below carries markdown="1" so the
# md_in_html extension re-parses its content as Markdown — without it, a
# caption whose text contains a citation link like `[49](url)` shows the
# raw `[49](url)` text instead of a working link, since md_in_html otherwise
# treats raw HTML blocks as opaque.
def expand_code_captions(text: str, counters: dict) -> str:
    def repl(m: re.Match) -> str:
        label = unescape_markdown(m.group(1))
        caption = unescape_markdown(m.group(2))
        counters["code"] = counters.get("code", 0) + 1
        n = counters["code"]
        anchor = f'<span id="{label}"></span>' if label else ""
        return (
            f'{anchor}\n\n<p class="thesis-caption" markdown="1"><em>Code {n} — {caption}</em></p>'
        )

    return re.sub(r"§§CODECAPTION§§([^§]*)§§([^§]*)§§", repl, text)


def expand_raw_tables(text: str, counters: dict) -> str:
    def repl(m: re.Match) -> str:
        label = unescape_markdown(m.group(1))
        caption = unescape_markdown(m.group(2))
        payload = m.group(3)
        data = json.loads(base64.b64decode(payload))
        header = data["header"]
        rows = data["rows"]
        counters["table"] = counters.get("table", 0) + 1
        n = counters["table"]

        parts = ['<table markdown="0">', "<thead><tr>"]
        for h in header:
            parts.append(f"<th>{h}</th>")
        parts.append("</tr></thead>")
        parts.append("<tbody>")
        for name, col2, col3 in rows:
            li2 = "".join(f"<li>{item}</li>" for item in col2)
            li3 = "".join(f"<li>{item}</li>" for item in col3)
            parts.append(
                f"<tr><td><strong>{name}</strong></td><td><ul>{li2}</ul></td><td><ul>{li3}</ul></td></tr>"
            )
        parts.append("</tbody></table>")

        anchor = f'<span id="{label}"></span>' if label else ""
        table_html = "".join(parts)
        caption_html = (
            f'<p class="thesis-caption" markdown="1"><em>Tableau {n} — {caption}</em></p>'
        )
        return f"{anchor}\n\n{table_html}\n\n{caption_html}"

    return re.sub(r"§§RAWTABLE§§([^§]*)§§([^§]*)§§([^§]*)§§", repl, text)


def fenced_divs_to_html(text: str) -> str:
    """Pandoc represents any LaTeX construct it turns into a Div — citeproc's
    bibliography (`::: {#ref-key .csl-entry}`), but also things like the
    abstract's `\\begin{otherlanguage}{french}` (`:::: {lang="fr"}`) — using
    its own `::: {attrs}` fenced-div syntax, which mkdocs/python-markdown
    doesn't understand (it renders the colons as literal text). Convert those
    fences to real `<div>` HTML, carrying over the id if there is one so the
    in-text citation links (`#ref-citekey`) have an anchor to jump to."""
    open_re = re.compile(r"^:{3,}\s*\{([^}]*)\}\s*$")
    close_re = re.compile(r"^:{3,}\s*$")

    def repl(line: str) -> str:
        m = open_re.match(line)
        if m:
            # markdown="1" (the md_in_html extension) re-enables Markdown
            # parsing inside this raw HTML block — without it, python-markdown
            # treats everything inside as opaque HTML and `*italic*` etc.
            # show up as literal asterisks instead of being rendered.
            id_m = re.search(r"#([^\s}]+)", m.group(1))
            id_attr = f' id="{id_m.group(1)}"' if id_m else ""
            return f'<div{id_attr} markdown="1">'
        if close_re.match(line):
            return "</div>"
        return line

    return "\n".join(repl(line) for line in text.split("\n"))


def fix_native_table_captions(text: str) -> str:
    """Pandoc emits successfully-parsed table captions as plain text ending
    in `{#tab:label}` — but that attr_list syntax only hides the braces and
    creates a real id when it's block-attached (a `{: #id}` line directly
    under the block, no blank line). Pandoc's own format doesn't qualify, so
    it shows up as literal visible curly-brace text. Replace it with a real
    anchor + a styled caption to match the Code/Tableau captions above."""

    def repl(m: re.Match) -> str:
        caption = m.group(1).strip()
        label = m.group(2)
        return (
            f'<span id="{label}"></span>\n\n'
            f'<p class="thesis-caption" markdown="1"><em>{caption}</em></p>'
        )

    return re.sub(r"^(.+?)\s*\{#(tab:[\w.-]+)\}\s*$", repl, text, flags=re.MULTILINE)


def number_equations(text: str, counters: dict) -> str:
    """Equations pandoc couldn't parse (cases/aligned environments) stay as
    raw TeX inside $$...$$ with their \\label{} intact. Give each one a
    visible (N) tag and an anchor so cross-references can resolve."""

    def repl(m: re.Match) -> str:
        block = m.group(0)
        labels = re.findall(r"\\label\{([^}]*)\}", block)
        if not labels:
            return block
        counters["eq"] = counters.get("eq", 0) + 1
        n = counters["eq"]
        # An `aligned` block can carry several \label{}s for its sub-lines
        # (e.g. a two-step update rule) — point all of them at this one
        # number rather than only anchoring the first.
        anchors = "".join(f'<span id="{label}"></span>' for label in labels)
        return f'{anchors}\n\n{block}\n\n<p class="thesis-caption" markdown="1"><em>({n})</em></p>'

    return re.sub(r"\$\$.*?\$\$", repl, text, flags=re.DOTALL)


def relative_href(from_path: Path, to_path: Path, anchor: str, *, html: bool) -> str:
    """`html=True` for raw HTML href="" attributes, which mkdocs never
    touches so they must already point at the built .html path. `html=False`
    for genuine `[text](...)` Markdown links — mkdocs rewrites a `.md`
    extension to the right URL itself at build time, and its strict-mode
    link checker only recognizes that form; pre-converting to `.html` there
    makes it flag the link as broken even though it works in practice."""
    if from_path == to_path:
        return f"#{anchor}"
    cur_rel = from_path.relative_to(DOCS)
    target_rel = to_path.relative_to(DOCS)
    depth = len(cur_rel.parts) - 1
    prefix = "../" * depth
    href = f"{prefix}{target_rel.as_posix()}"
    if html:
        href = href.replace(".md", ".html")
    return f"{href}#{anchor}"


def fix_citation_links(texts: dict[Path, str], bib_path: Path) -> None:
    """Citation links (`[text](#ref-key)` / `<a href="#ref-key">`) are written
    assuming the bibliography is on the same page. Since it now lives on its
    own page (one combined list instead of one per chapter), point them at
    that page instead — otherwise every citation link 404s in place."""
    if bib_path not in texts:
        return

    for path in list(texts):
        if path == bib_path:
            continue
        text = texts[path]
        text = re.sub(
            r"\]\(#(ref-[\w-]+)\)",
            lambda m, path=path: f"]({relative_href(path, bib_path, m.group(1), html=False)})",
            text,
        )
        text = re.sub(
            r'href="#(ref-[\w-]+)"',
            lambda m, path=path: f'href="{relative_href(path, bib_path, m.group(1), html=True)}"',
            text,
        )
        texts[path] = text


def fix_cross_page_link_attrs(texts: dict[Path, str], anchor_location: dict[str, Path]) -> None:
    """pandoc's `link_attributes` extension (enabled for the bibliography fix)
    changed how it writes \\ref{}-style cross-references in the combined
    chapters+appendices pass: instead of raw HTML <a data-reference-type=...>
    (which fix_cross_page_link_attrs's sibling pass already handles), it now
    emits `[N](#label){reference-type="ref" reference="label"}` — a genuine
    Markdown link with a same-page-only href. Pandoc resolves the *number*
    correctly because it saw the whole combined document, but after
    split_combined.py splits that into separate chapter files, `#label` only
    works when label happens to live on the same page. Point it at the right
    page otherwise."""
    link_re = re.compile(r'\]\(#([^)]+)\)(\{reference-type="ref" reference="[^"]+"\})')

    for path in list(texts):
        text = texts[path]

        def repl(m: re.Match, path: Path = path) -> str:
            label, attrs = m.group(1), m.group(2)
            target_path = anchor_location.get(label)
            if target_path is None or target_path == path:
                return m.group(0)
            return f"]({relative_href(path, target_path, label, html=False)}){attrs}"

        texts[path] = link_re.sub(repl, text)


def add_image_alt_text(text: str) -> str:
    """Pandoc carries a figure's caption only in <figcaption>, never copies it
    into the <img>'s alt attribute — every image on the site ends up with no
    alt text at all (bad for accessibility and image search). The two are
    always adjacent in the generated HTML, for both single-image figures and
    each subfigure of a multi-image one, so this doesn't need to know
    anything about the surrounding <figure> nesting."""

    def repl(m: re.Match) -> str:
        attrs, caption_html = m.group(1), m.group(2)
        if "alt=" in attrs:
            return m.group(0)
        alt_text = re.sub(r"<[^>]+>", "", caption_html).strip()
        alt_text = html.unescape(alt_text).replace('"', "'")
        return f'<img {attrs} alt="{alt_text}" />\n<figcaption>{caption_html}</figcaption>'

    return re.sub(
        r"<img ([^>]*?)/>\s*\n<figcaption>(.*?)</figcaption>", repl, text, flags=re.DOTALL
    )


# Pages whose content doesn't read as natural prose (a numbered reference
# list, a glossary table) get a fixed description instead of trying to
# extract one from their first paragraph.
FIXED_DESCRIPTIONS = {
    "bibliography.md": "Bibliographie numérotée par ordre de citation du mémoire de Master.",
    "glossary.md": "Glossaire des termes, acronymes et abréviations du mémoire de Master.",
}


def add_meta_description(text: str, path: Path) -> str:
    """Every generated page currently inherits the same global
    site_description, so every search-result snippet for the whole site is
    identical. Give each page its own, derived from its first real paragraph
    (stripped of markup) and capped to a typical search-snippet length."""
    if text.startswith("---\n"):
        return text  # docs/index.md is hand-written with its own description
    rel = path.relative_to(DOCS).as_posix()
    fixed = FIXED_DESCRIPTIONS.get(rel)
    if fixed:
        description = fixed
    else:
        body = re.sub(r"^#.*$", "", text, count=1, flags=re.MULTILINE)
        para_match = re.search(r"^[A-Za-zÀ-ÿ].+$", body, re.MULTILINE)
        if not para_match:
            return text
        para = para_match.group(0)
        para = re.sub(r"<[^>]+>", "", para)
        para = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", para)
        para = html.unescape(para)
        # Drop leftover numeric citation markers (e.g. "[1]", "[2, 3]") —
        # meaningful in body text, just noise in a search-snippet description.
        para = re.sub(r"\s*\[\d+(?:,\s*\d+)*\]\.?", "", para).strip()
        if len(para) > 155:
            para = para[:155].rsplit(" ", 1)[0] + "…"
        description = para
    description = description.replace('"', "'")
    return f'---\ndescription: "{description}"\n---\n\n{text}'


def harvest_resolved_numbers(texts: dict[Path, str]) -> dict[str, str]:
    """Pandoc auto-numbers figures/tables it parses natively as chapter.N
    (e.g. "6.1"), but only bakes that number into the *in-text* cross
    reference — the figure/table's own caption stays bare, with no "Figure
    6.1" prefix at all. Harvest the number from any already-resolved
    `[6.1](...#fig:label)` / `[6.1](...#tab:label)` link so the caption
    passes below can prefix the caption itself the same way."""
    numbers: dict[str, str] = {}
    pattern = re.compile(r"\[(\d+(?:\.\d+)?)\]\([^)]*#(fig|tab):([\w-]+)\)")
    for text in texts.values():
        for m in pattern.finditer(text):
            numbers[f"{m.group(2)}:{m.group(3)}"] = m.group(1)
    return numbers


# Combined-pass files only — chapters/00-resume.md is its own separate
# pandoc run with no chapter prefix in its numbering, so it isn't part of
# this scheme and stays on harvest_resolved_numbers alone (see below).
CHAPTER_INDEX = {
    DOCS / "chapters" / "01-introduction.md": 1,
    DOCS / "chapters" / "02-analysis.md": 2,
    DOCS / "chapters" / "03-modele.md": 3,
    DOCS / "chapters" / "04-implementation.md": 4,
    DOCS / "chapters" / "05-conclusions.md": 5,
    DOCS / "appendices" / "A1-fondamentaux-ml.md": 6,
    DOCS / "appendices" / "A2-fondamentaux-energie.md": 7,
}


def compute_structural_numbers(texts: dict[Path, str]) -> dict[str, str]:
    """harvest_resolved_numbers only finds a number for labels that happen
    to be \\ref'd somewhere in the prose — anything never referenced (a
    surprisingly common ~12% of figures here) gets no number at all, even
    though pandoc's own internal chapter.N counter clearly still ticks
    forward for it (confirmed empirically: numbers harvested on either side
    of an unreferenced figure/table have no gap, e.g. ...6.2, [unref], 6.4...
    means the unreferenced one really is 6.3). Recompute every number
    directly from document order instead of relying on \\ref having been
    used.

    Figures need a post-order walk, not a flat scan: a figure that groups
    several individually-\\label'd subfigures is numbered by pandoc *after*
    all its children (confirmed: a group's own number, e.g. 2.21, exceeds
    every one of its subfigures', e.g. 2.16-2.20, even though the group's
    opening tag comes first in the HTML) — so each nested figure must be
    numbered before the figure containing it."""
    figure_open_re = re.compile(r'<figure id="(fig:[\w-]+)"[^>]*>')
    table_open_re = re.compile(r'<table id="(tab:[\w-]+)">|<span id="(tab:[\w-]+)"></span>')

    def walk_figures(
        text: str, counter: list[int], chapter_n: int, numbers: dict[str, str]
    ) -> None:
        i = 0
        while True:
            m = figure_open_re.search(text, i)
            if not m:
                break
            label = m.group(1)
            depth = 1
            j = m.end()
            while depth > 0:
                next_open = text.find("<figure", j)
                next_close = text.find("</figure>", j)
                if next_close == -1:
                    j = len(text)
                    break
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    j = next_open + len("<figure")
                else:
                    depth -= 1
                    j = next_close + len("</figure>")
            block_end = j - len("</figure>") if j <= len(text) else j
            walk_figures(text[m.end() : block_end], counter, chapter_n, numbers)
            counter[0] += 1
            numbers[label] = f"{chapter_n}.{counter[0]}"
            i = j

    numbers: dict[str, str] = {}
    for path, chapter_n in CHAPTER_INDEX.items():
        text = texts.get(path)
        if text is None:
            continue
        walk_figures(text, [0], chapter_n, numbers)
        for tab_counter, m in enumerate(table_open_re.finditer(text), start=1):
            label = m.group(1) or m.group(2)
            numbers[label] = f"{chapter_n}.{tab_counter}"
    return numbers


def add_figure_caption_numbers(text: str, numbers: dict[str, str]) -> str:
    """Prefix each figure's *own* caption with "Figure N — " using the number
    harvested from its in-text references. Most subfigures are a bare nested
    <figure> (no id, e.g. "Original"/"Ground truth") and are correctly left
    alone — but some subfigures carry their own \\label (and so their own
    `id="fig:..."` and their own harvested number), and recursing into each
    outer figure's content is what numbers those too instead of silently
    skipping every figure nested inside another one."""
    out = []
    i = 0
    open_re = re.compile(r'<figure id="(fig:[\w-]+)"[^>]*>')
    while True:
        m = open_re.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i : m.end()])
        label = m.group(1)
        depth = 1
        j = m.end()
        while depth > 0:
            next_open = text.find("<figure", j)
            next_close = text.find("</figure>", j)
            if next_close == -1:
                j = len(text)
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                j = next_open + len("<figure")
            else:
                depth -= 1
                j = next_close + len("</figure>")
        block_end = j - len("</figure>") if j <= len(text) and depth == 0 else j
        block = text[m.end() : block_end]

        block = add_figure_caption_numbers(block, numbers)

        number = numbers.get(label)
        if number:
            last_idx = block.rfind("<figcaption>")
            if last_idx != -1:
                close_idx = block.find("</figcaption>", last_idx)
                inner = block[last_idx + len("<figcaption>") : close_idx]
                if not inner.startswith("Figure "):
                    block = (
                        block[:last_idx]
                        + f"<figcaption>Figure {number} — {inner}</figcaption>"
                        + block[close_idx + len("</figcaption>") :]
                    )
        out.append(block)
        if j <= len(text):
            out.append("</figure>")
        i = j

    return "".join(out)


def add_native_table_caption_numbers(text: str, numbers: dict[str, str]) -> str:
    """Same idea as add_figure_caption_numbers, for the two different shapes
    pandoc uses for a table caption depending on how complex the table is:
    a real <table><caption> for ones with colspan/rowspan, or the
    span+styled-<p> form fix_native_table_captions produces for plain pipe
    tables. Skip anything already prefixed by our own Code/Tableau counters
    (RAWTABLE custom tables) — those aren't in `numbers` anyway since pandoc
    never saw them, but the explicit check makes that not load-bearing."""

    def table_repl(m: re.Match) -> str:
        label, caption = m.group(1), m.group(2)
        number = numbers.get(label)
        if not number:
            return m.group(0)
        return f'<table id="{label}">\n<caption>Tableau {number} — {caption}</caption>'

    text = re.sub(
        r'<table id="(tab:[\w-]+)">\s*<caption>(.*?)</caption>',
        table_repl,
        text,
        flags=re.DOTALL,
    )

    def span_repl(m: re.Match) -> str:
        label, caption = m.group(1), m.group(2)
        if re.match(r"^(Tableau|Code) \d", caption):
            return m.group(0)
        number = numbers.get(label)
        if not number:
            return m.group(0)
        return (
            f'<span id="{label}"></span>\n\n'
            f'<p class="thesis-caption" markdown="1"><em>Tableau {number} — {caption}</em></p>'
        )

    return re.sub(
        r'<span id="(tab:[\w-]+)"></span>\n\n'
        r'<p class="thesis-caption" markdown="1"><em>(.*?)</em></p>',
        span_repl,
        text,
        flags=re.DOTALL,
    )


def build_list_pages(texts: dict[Path, str]) -> str:
    """A standalone page mirroring this thesis's LaTeX \\listoffigures /
    \\listoftables / its custom "Liste de blocs de code" — one section per
    type, each entry linking straight to the figure/table/code block."""
    figures: list[tuple[tuple, str, str, str]] = []
    tables: list[tuple[tuple, str, str, str]] = []
    code: list[tuple[tuple, str, str, str]] = []

    fig_re = re.compile(
        r'<figure id="(fig:[\w-]+)"[^>]*>.*?<figcaption>Figure ([\d.]+) — (.*?)</figcaption>',
        re.DOTALL,
    )
    table_re = re.compile(
        r'(?:<table id="(tab:[\w-]+)">\s*<caption>|<span id="(tab:[\w-]+)"></span>\s*\n\n'
        r'<p class="thesis-caption" markdown="1"><em>)Tableau ([\d.]+) — '
        r"(.*?)(?:</caption>|</em></p>)",
        re.DOTALL,
    )
    code_re = re.compile(
        r'<span id="(code:[\w-]+)"></span>\s*\n\n<p class="thesis-caption" markdown="1"><em>'
        r"Code (\d+) — (.*?)</em></p>",
        re.DOTALL,
    )

    def sort_key(number: str) -> tuple:
        return tuple(int(p) for p in number.split("."))

    # The abstract/résumé (chapters/00-resume.md) is converted by its own,
    # separate pandoc pass — its figures/tables get plain "1", "2" numbers
    # with no chapter prefix, since pandoc never saw it as part of the
    # combined body. Mixed into one list alongside the main body's "2.1",
    # "6.3" chapter.N numbers that's just confusing, and every figure/table
    # in the abstract duplicates one already listed from its real chapter.
    skip_paths = {DOCS / "chapters" / "00-resume.md"}

    for path, text in texts.items():
        if path in skip_paths:
            continue
        # Genuine `[text](url)` Markdown links need the source `.md`
        # extension — mkdocs rewrites that to the right URL itself at build
        # time, and only recognizes that form in its strict-mode link check.
        rel = path.relative_to(DOCS).as_posix()
        for m in fig_re.finditer(text):
            label, number, caption = m.group(1), m.group(2), m.group(3)
            caption = re.sub(r"<[^>]+>", "", caption).strip()
            figures.append((sort_key(number), number, caption, f"{rel}#{label}"))
        for m in table_re.finditer(text):
            label = m.group(1) or m.group(2)
            number, caption = m.group(3), m.group(4)
            caption = re.sub(r"<[^>]+>", "", caption).strip()
            tables.append((sort_key(number), number, caption, f"{rel}#{label}"))
        for m in code_re.finditer(text):
            label, number, caption = m.group(1), m.group(2), m.group(3)
            caption = re.sub(r"<[^>]+>", "", caption).strip()
            code.append((sort_key(number), number, caption, f"{rel}#{label}"))

    figures.sort(key=lambda r: r[0])
    tables.sort(key=lambda r: r[0])
    code.sort(key=lambda r: r[0])

    lines = [
        "---",
        'description: "Liste des figures, tableaux et blocs de code du mémoire de Master."',
        "---",
        "",
        "# Listes des figures, tableaux et codes",
        "",
        "## Liste des figures",
        "",
    ]
    for _, number, caption, href in figures:
        lines.append(f"- [Figure {number} — {caption}]({href})")
    lines += ["", "## Liste des tableaux", ""]
    for _, number, caption, href in tables:
        lines.append(f"- [Tableau {number} — {caption}]({href})")
    lines += ["", "## Liste des blocs de code", ""]
    for _, number, caption, href in code:
        lines.append(f"- [Code {number} — {caption}]({href})")
    lines.append("")
    return "\n".join(lines)


# The thesis's own \newfloat{code}{...} has no \counterwithin{chapter}, so
# the original LaTeX numbers code listings continuously across the whole
# document ("Code 1" through "Code N"), unlike figures/tables which restart
# per chapter. Process files in actual reading order (not the alphabetical
# order rglob gives, which would put appendices before chapter 5) so that
# global counter — and the list-of-X pages below — come out in the right
# order.
READING_ORDER = [
    DOCS / "index.md",
    DOCS / "chapters" / "00-resume.md",
    DOCS / "chapters" / "01-introduction.md",
    DOCS / "chapters" / "02-analysis.md",
    DOCS / "chapters" / "03-modele.md",
    DOCS / "chapters" / "04-implementation.md",
    DOCS / "chapters" / "05-conclusions.md",
    DOCS / "appendices" / "A1-fondamentaux-ml.md",
    DOCS / "appendices" / "A2-fondamentaux-energie.md",
    DOCS / "bibliography.md",
    DOCS / "glossary.md",
]


def main() -> None:
    all_files = set(DOCS.rglob("*.md"))
    md_files = [p for p in READING_ORDER if p in all_files]
    md_files += sorted(all_files - set(md_files))

    texts = {}
    code_counters: dict = {}
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        counters: dict = {}
        text = fix_bare_url_autolinks(text)
        text = fix_bracket_escapes(text)
        text = fix_math_escaping(text)
        text = expand_code_blocks(text)
        text = expand_code_captions(text, code_counters)
        text = expand_raw_tables(text, counters)
        text = number_equations(text, counters)
        text = fix_native_table_captions(text)
        text = fenced_divs_to_html(text)
        texts[path] = text

    # Build a global label registry: label -> (path, display_text)
    registry: dict[str, tuple[Path, str]] = {}
    caption_after_span = re.compile(
        r'\A(?:<span id="[^"]+"></span>)*\n\n(?:(?!<span id=").)*?'
        r'<p class="thesis-caption" markdown="1"><em>(.*?)</em></p>',
        re.DOTALL,
    )
    # A real LaTeX \ref{} to a Code/Tableau float resolves to just its bare
    # number (e.g. "Le Code 3"), never its caption text. But the caption
    # text captured above for these already carries a "Code 3 — ..." /
    # "Tableau 3 — ..." prefix (added at creation time, before this registry
    # is built) — using it verbatim as ref display text doubles the word
    # ("Le Code Code 3 — ..."). Strip back down to the number for those.
    caption_number_prefix = re.compile(r"^(?:Code|Tableau) ([\d.]+) — ")

    def _ref_display_text(caption: str) -> str:
        m = caption_number_prefix.match(caption)
        return m.group(1) if m else caption

    for path, text in texts.items():
        # A block (e.g. an `aligned` equation with two \label{}s) can have
        # several adjacent anchor spans sharing one caption further down.
        for sm in re.finditer(r'<span id="([^"]+)"></span>', text):
            cap_m = caption_after_span.match(text[sm.end() :])
            if cap_m:
                registry[sm.group(1)] = (path, _ref_display_text(cap_m.group(1)))
        for m in re.finditer(r"^(#{1,6})\s+(.*?)\s*\{#([^}]+)\}\s*$", text, re.MULTILINE):
            registry[m.group(3)] = (path, m.group(2).strip())

    # Resolve unresolved refs. pandoc's link_attributes extension (needed for
    # the bibliography fix) made it switch every \ref{}-style output — both
    # the ones it resolves itself and the ones it can't — to one Markdown
    # form: `[text](#label){reference-type="ref" reference="label"}`. For
    # labels pandoc never builds an anchor/number for (equations that fail to
    # parse as Math, and this site's own code-listing sentinels), `text` is
    # just the raw label, still wrapped in the HTML-entity brackets
    # fix_bracket_escapes already converted it to.
    ref_re = re.compile(r'\[([^\]]*)\]\(#([^)]+)\)(\{reference-type="ref" reference="[^"]+"\})')

    for path in list(texts):
        text = texts[path]

        def repl(m: re.Match, path: Path = path) -> str:
            visible, label, attrs = m.group(1), m.group(2), m.group(3)
            unescaped_label = unescape_markdown(label)
            if unescape_markdown(visible) != f"&#91;{unescaped_label}&#93;":
                return m.group(0)
            target = registry.get(unescaped_label)
            if target is None:
                return m.group(0)
            target_path, display_text = target
            href = relative_href(path, target_path, unescaped_label, html=False)
            return f"[{display_text}]({href}){attrs}"

        texts[path] = ref_re.sub(repl, text)

    fix_citation_links(texts, DOCS / "bibliography.md")

    # Every anchor on the site, regardless of how it was produced (a figure's
    # own id, a span/div anchor, or a heading's `{#id}`), so the next pass can
    # tell whether a label lives on the current page or a different one.
    anchor_location: dict[str, Path] = {}
    for path, text in texts.items():
        for m in re.finditer(r'<[a-zA-Z]+[^>]*\bid="([^"]+)"', text):
            anchor_location[m.group(1)] = path
        for m in re.finditer(r"^#{1,6}\s+.*\{#([^}\s]+)", text, re.MULTILINE):
            anchor_location[m.group(1)] = path
    fix_cross_page_link_attrs(texts, anchor_location)

    # Prefix every figure's/native table's own caption with "Figure N — " /
    # "Tableau N — ". Compute the number directly from document structure
    # for the combined-pass chapters/appendices (covers every figure/table,
    # not just ones \ref'd somewhere); fall back to harvesting an already-
    # resolved in-text reference for chapters/00-resume.md, which is its own
    # separate pandoc pass and outside that chapter.N numbering scheme.
    numbers = compute_structural_numbers(texts)
    for label, number in harvest_resolved_numbers(texts).items():
        numbers.setdefault(label, number)
    for path, text in texts.items():
        text = add_figure_caption_numbers(text, numbers)
        text = add_native_table_caption_numbers(text, numbers)
        texts[path] = text

    list_page = DOCS / "lists.md"
    texts[list_page] = build_list_pages(texts)

    for path, text in texts.items():
        text = add_image_alt_text(text)
        text = add_meta_description(text, path)
        texts[path] = text

    for path, text in texts.items():
        path.write_text(text, encoding="utf-8")

    print(
        "Fixed math escaping, expanded code/table sentinels, and resolved "
        f"cross-references in {len(md_files)} files"
    )


if __name__ == "__main__":
    main()
