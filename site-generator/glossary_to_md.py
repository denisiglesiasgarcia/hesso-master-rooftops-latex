#!/usr/bin/env python3
"""Convert glossary.tex (glossaries package) to a Markdown table.

Run after convert_thesis.sh — it needs docs/bibliography.md to already exist
so `\\cite{}` commands inside glossary descriptions can be resolved to the
same numbered links used everywhere else on the site.

Handles:
    \\newglossaryentry{<label>}{name=..., description={...}}
    \\newacronym{<label>}{<abbrv>}{<full>}
Skips `%`-comment lines (the file's own format/example comments otherwise
get matched as if they were real entries).
"""

import re
from pathlib import Path

SRC = Path("03-tail/glossary.tex")
BIB = Path("docs/bibliography.md")
DST = Path("docs/glossary.md")


def strip_comments(text: str) -> str:
    """Drop `%...` to end of line, but keep an escaped `\\%` (literal percent)."""
    return re.sub(r"(?<!\\)%.*", "", text)


def read_balanced_group(text: str, start: int) -> tuple[str, int]:
    """text[start] must be '{'. Returns (inner_content, index_after_closing_brace)."""
    depth = 1
    j = start + 1
    while depth > 0 and j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
        j += 1
    return text[start + 1 : j - 1], j


def find_arg(text: str, start: int) -> tuple[str, int]:
    """Skip whitespace from `start`, then read one balanced {...} group."""
    j = start
    while j < len(text) and text[j] in " \t\r\n":
        j += 1
    if j >= len(text) or text[j] != "{":
        raise ValueError(f"expected '{{' at {j}: {text[j : j + 30]!r}")
    return read_balanced_group(text, j)


def parse_settings(settings: str) -> dict[str, str]:
    """Split a glossaryentry settings block on top-level commas into key=value
    pairs (value may itself be a brace-wrapped group, e.g. description={...})."""
    fields: dict[str, str] = {}
    i = 0
    while i < len(settings):
        eq = settings.find("=", i)
        if eq == -1:
            break
        key = settings[i:eq].strip().strip(",").strip()
        j = eq + 1
        while j < len(settings) and settings[j] in " \t\r\n":
            j += 1
        if j < len(settings) and settings[j] == "{":
            value, j = read_balanced_group(settings, j)
        else:
            comma = settings.find(",", j)
            value = settings[j : comma if comma != -1 else len(settings)].strip()
            j = comma if comma != -1 else len(settings)
        fields[key] = value.strip()
        i = j + 1
    return fields


def clean(text: str) -> str:
    """Strip basic LaTeX markup that commonly appears inside descriptions."""
    text = re.sub(r"\\textit\{([^}]+)\}", r"*\1*", text)
    text = re.sub(r"\\textbf\{([^}]+)\}", r"**\1**", text)
    text = re.sub(r"\\\\", " ", text)
    return text.strip().replace("\n", " ")


def load_citation_numbers() -> dict[str, str]:
    """Map bib citation key -> its already-resolved [N] number, by reading
    the anchors fix_text.py left in the combined bibliography page."""
    if not BIB.exists():
        return {}
    text = BIB.read_text(encoding="utf-8")
    numbers = {}
    for m in re.finditer(r'<div id="ref-([\w-]+)"[^>]*>\s*&#91;(\d+)&#93;', text):
        numbers[m.group(1)] = m.group(2)
    return numbers


def resolve_citations(text: str, citation_numbers: dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        keys = m.group(1).split(",")
        links = []
        for key in keys:
            key = key.strip()
            n = citation_numbers.get(key)
            # Match the rest of the site's citation style: a visible "[N]"
            # with only the number itself as the link, brackets as plain
            # text around it. Markdown `[text](url)` would otherwise consume
            # the brackets as link-text delimiters and render bare "N" with
            # no brackets at all — and glossary_to_md.py runs after
            # fix_text.py's bracket-to-entity pass, so plain `\[`/`\]` here
            # would never get converted and could still collide with
            # MathJax's `\[...\]` math-block syntax.
            link = f"[{n}](bibliography.md#ref-{key})" if n else key
            links.append(f"&#91;{link}&#93;")
        return "".join(links)

    return re.sub(r"\\cite\{([^}]*)\}", repl, text)


def main() -> None:
    content = strip_comments(SRC.read_text(encoding="utf-8"))
    citation_numbers = load_citation_numbers()
    rows: list[tuple[str, str, str]] = []  # (key, name, description)

    for m in re.finditer(r"\\newglossaryentry\s*\{([^}]+)\}", content):
        key = m.group(1).strip()
        settings, _ = find_arg(content, m.end())
        fields = parse_settings(settings)
        name = clean(fields.get("name", key))
        description = resolve_citations(fields.get("description", ""), citation_numbers)
        rows.append((key, name, clean(description)))

    for m in re.finditer(r"\\newacronym(?:\[[^\]]*\])?\s*\{([^}]+)\}", content):
        key = m.group(1).strip()
        abbr, after = find_arg(content, m.end())
        full, _ = find_arg(content, after)
        rows.append((key, clean(abbr), clean(full)))

    if not rows:
        print("No entries matched — open glossary.tex and adjust the regex patterns.")
        return

    rows.sort(key=lambda r: r[1].lower())

    lines = ["# Glossaire", "", "| Terme | Définition |", "|---|---|"]
    for key, name, description in rows:
        lines.append(f'| <span id="gloss-{key}">{name}</span> | {description} |')

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} entries to {DST}")


if __name__ == "__main__":
    main()
