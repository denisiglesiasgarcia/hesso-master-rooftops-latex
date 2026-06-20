#!/usr/bin/env python3
"""Link every `\\gls{}`/`\\acrshort{}`/`\\acrlong{}` usage across the site to
its entry on the glossary page. Pandoc renders each occurrence as a bare
<span data-acronym-label="key" ...>text</span> with no link at all, and the
visible text is just the lowercase \\gls{} key (e.g. "sia") rather than the
term's actual display form ("SIA"). Wrap it in an <a> pointing at the
matching `id="gloss-key"` anchor glossary_to_md.py writes for that same key,
and replace the visible text with the glossary's own defined name, so every
acronym/term in the text is both clickable and correctly cased.

Run last, after glossary_to_md.py has written docs/glossary.md.
"""

import re
from pathlib import Path

DOCS = Path("docs")
GLOSSARY = DOCS / "glossary.md"

SPAN_RE = re.compile(r'<span data-acronym-label="([\w-]+)"([^>]*)>(.*?)</span>')
GLOSSARY_ENTRY_RE = re.compile(r'<span id="gloss-([\w-]+)">(.*?)</span>')


def relative_href(from_path: Path, to_path: Path, anchor: str) -> str:
    if from_path == to_path:
        return f"#{anchor}"
    cur_rel = from_path.relative_to(DOCS)
    target_rel = to_path.relative_to(DOCS)
    depth = len(cur_rel.parts) - 1
    prefix = "../" * depth
    href = f"{prefix}{target_rel.as_posix()}".replace(".md", ".html")
    return f"{href}#{anchor}"


def load_display_names() -> dict[str, str]:
    text = GLOSSARY.read_text(encoding="utf-8")
    return dict(GLOSSARY_ENTRY_RE.findall(text))


def main() -> None:
    if not GLOSSARY.exists():
        print("docs/glossary.md not found, skipping acronym links")
        return

    display_names = load_display_names()
    count = 0
    for path in sorted(DOCS.rglob("*.md")):
        if path == GLOSSARY:
            continue
        text = path.read_text(encoding="utf-8")

        def repl(m: re.Match, path: Path = path) -> str:
            nonlocal count
            count += 1
            key, attrs, original_text = m.group(1), m.group(2), m.group(3)
            href = relative_href(path, GLOSSARY, f"gloss-{key}")
            name = display_names.get(key, original_text)
            span = f'<span data-acronym-label="{key}"{attrs}>{name}</span>'
            return f'<a href="{href}">{span}</a>'

        new_text = SPAN_RE.sub(repl, text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")

    print(f"Linked {count} acronym/glossary-term occurrences to {GLOSSARY}")


if __name__ == "__main__":
    main()
