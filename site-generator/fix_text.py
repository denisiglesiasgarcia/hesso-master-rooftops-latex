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
        return m.group(0).replace(r"\_", "_").replace(r"\|", "|")

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


def expand_code_captions(text: str, counters: dict) -> str:
    def repl(m: re.Match) -> str:
        label = unescape_markdown(m.group(1))
        caption = unescape_markdown(m.group(2))
        counters["code"] = counters.get("code", 0) + 1
        n = counters["code"]
        anchor = f'<span id="{label}"></span>' if label else ""
        return f'{anchor}\n\n<p class="thesis-caption"><em>Code {n} — {caption}</em></p>'

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
        caption_html = f'<p class="thesis-caption"><em>Tableau {n} — {caption}</em></p>'
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
        return f'<span id="{label}"></span>\n\n<p class="thesis-caption"><em>{caption}</em></p>'

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
        return f'{anchors}\n\n{block}\n\n<p class="thesis-caption"><em>({n})</em></p>'

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


def main() -> None:
    md_files = sorted(DOCS.rglob("*.md"))
    texts = {}
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        counters: dict = {}
        text = fix_bare_url_autolinks(text)
        text = fix_bracket_escapes(text)
        text = fix_math_escaping(text)
        text = expand_code_blocks(text)
        text = expand_code_captions(text, counters)
        text = expand_raw_tables(text, counters)
        text = number_equations(text, counters)
        text = fix_native_table_captions(text)
        text = fenced_divs_to_html(text)
        texts[path] = text

    # Build a global label registry: label -> (path, display_text)
    registry: dict[str, tuple[Path, str]] = {}
    caption_after_span = re.compile(
        r'\A(?:<span id="[^"]+"></span>)*\n\n(?:(?!<span id=").)*?'
        r'<p class="thesis-caption"><em>(.*?)</em></p>',
        re.DOTALL,
    )
    for path, text in texts.items():
        # A block (e.g. an `aligned` equation with two \label{}s) can have
        # several adjacent anchor spans sharing one caption further down.
        for sm in re.finditer(r'<span id="([^"]+)"></span>', text):
            cap_m = caption_after_span.match(text[sm.end() :])
            if cap_m:
                registry[sm.group(1)] = (path, cap_m.group(1))
        for m in re.finditer(r"^(#{1,6})\s+(.*?)\s*\{#([^}]+)\}\s*$", text, re.MULTILINE):
            registry[m.group(3)] = (path, m.group(2).strip())

    # Resolve unresolved refs: <a href="#LABEL" data-reference-type="ref"
    # data-reference="LABEL">[label-text]</a> where the visible text is just
    # the raw label (pandoc couldn't build a real anchor/number for it).
    ref_re = re.compile(
        r'<a href="#([^"]+)" data-reference-type="ref" data-reference="([^"]+)">(\[[^\]]*\])</a>'
    )

    for path in list(texts):
        text = texts[path]

        def repl(m: re.Match, path: Path = path) -> str:
            label = m.group(1)
            unescaped_label = unescape_markdown(label)
            visible = unescape_markdown(m.group(3))
            if visible != f"[{unescaped_label}]":
                return m.group(0)
            target = registry.get(unescaped_label)
            if target is None:
                return m.group(0)
            target_path, display_text = target
            href = relative_href(path, target_path, unescaped_label, html=True)
            return f'<a href="{href}">{display_text}</a>'

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
