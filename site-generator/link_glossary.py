#!/usr/bin/env python3
"""Link every `\\gls{}`/`\\acrshort{}`/`\\acrlong{}` usage across the site to
its entry on the glossary page. Pandoc renders each occurrence as a bare
<span data-acronym-label="key" ...>text</span> with no link at all; wrap it in
an <a> pointing at the matching `id="gloss-key"` anchor glossary_to_md.py
writes for that same key, so every acronym/term in the text is clickable.

Run last, after glossary_to_md.py has written docs/glossary.md.
"""

import re
from pathlib import Path

DOCS = Path("docs")
GLOSSARY = DOCS / "glossary.md"

SPAN_RE = re.compile(r'<span data-acronym-label="([\w-]+)"[^>]*>.*?</span>')


def relative_href(from_path: Path, to_path: Path, anchor: str) -> str:
    if from_path == to_path:
        return f"#{anchor}"
    cur_rel = from_path.relative_to(DOCS)
    target_rel = to_path.relative_to(DOCS)
    depth = len(cur_rel.parts) - 1
    prefix = "../" * depth
    href = f"{prefix}{target_rel.as_posix()}".replace(".md", ".html")
    return f"{href}#{anchor}"


def main() -> None:
    if not GLOSSARY.exists():
        print("docs/glossary.md not found, skipping acronym links")
        return

    count = 0
    for path in sorted(DOCS.rglob("*.md")):
        if path == GLOSSARY:
            continue
        text = path.read_text(encoding="utf-8")

        def repl(m: re.Match, path: Path = path) -> str:
            nonlocal count
            count += 1
            href = relative_href(path, GLOSSARY, f"gloss-{m.group(1)}")
            return f'<a href="{href}">{m.group(0)}</a>'

        new_text = SPAN_RE.sub(repl, text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")

    print(f"Linked {count} acronym/glossary-term occurrences to {GLOSSARY}")


if __name__ == "__main__":
    main()
