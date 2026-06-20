#!/usr/bin/env python3
"""Split the single combined chapters+appendices Markdown (produced by one
pandoc+citeproc pass, so citation numbers and the bibliography are globally
consistent) back into the per-chapter files mkdocs needs, plus a standalone
bibliography page.

Usage: split_combined.py <combined.md> <bib_title> <out1> <out2> ... <outN>
The N output paths must be given in the same order as the chapters appear in
the combined file.
"""

import re
import sys
from pathlib import Path

CHAPTER_HEADING = re.compile(r"^# .*\{#chap:[\w-]+\}\s*$", re.MULTILINE)
# A footnote definition: `[^label]:` plus any immediately-following indented
# continuation lines (pandoc's way of representing multi-line footnotes).
FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:.*(?:\n(?:[ \t]+\S.*)?)*", re.MULTILINE)


def extract_footnote_defs(text: str) -> tuple[str, dict[str, str]]:
    """Pandoc always collects footnote *definitions* at the very end of the
    document, even though the inline `[^label]` markers stay put in their
    original chapter — so naively splitting by chapter heading leaves every
    footnote's content stranded on whatever page happens to be last. Pull the
    definitions out here; the caller re-attaches each one to whichever
    chapter slice actually contains its marker."""
    defs: dict[str, str] = {}

    def repl(m: re.Match) -> str:
        defs[m.group(1)] = m.group(0).strip()
        return ""

    text = FOOTNOTE_DEF.sub(repl, text)
    return text, defs


def main() -> None:
    combined_path = Path(sys.argv[1])
    bib_title = sys.argv[2]
    out_paths = [Path(p) for p in sys.argv[3:]]

    text = combined_path.read_text(encoding="utf-8")
    text, footnote_defs = extract_footnote_defs(text)
    # Drop the throwaway paragraph convert_thesis.sh appended so glossary-only
    # citations get a number and a bibliography entry — its citations are
    # already resolved elsewhere by being cited for real in the glossary; this
    # paragraph itself has no content worth keeping.
    text = re.sub(r"^GLOSSARYCITEPLACEHOLDER.*$\n*", "", text, flags=re.MULTILINE)

    bib_heading = re.search(
        rf"^# {re.escape(bib_title)}\s*(?:\{{[^}}]*\}})?\s*$", text, re.MULTILINE
    )
    if bib_heading:
        body, bibliography = text[: bib_heading.start()], text[bib_heading.start() :]
    else:
        body, bibliography = text, ""

    starts = [m.start() for m in CHAPTER_HEADING.finditer(body)]
    if len(starts) != len(out_paths):
        raise SystemExit(f"Expected {len(out_paths)} chapter headings, found {len(starts)}")
    starts.append(len(body))

    marker_re = re.compile(r"\[\^([^\]]+)\]")
    for out_path, start, end in zip(out_paths, starts[:-1], starts[1:], strict=True):
        chunk = body[start:end].strip()
        used = dict.fromkeys(marker_re.findall(chunk))  # dedup, keep order
        defs = [footnote_defs[label] for label in used if label in footnote_defs]
        if defs:
            chunk += "\n\n" + "\n\n".join(defs)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(chunk + "\n", encoding="utf-8")

    if bibliography:
        bib_path = Path("docs/bibliography.md")
        bib_path.write_text(bibliography.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
