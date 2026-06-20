#!/usr/bin/env python3
"""Post-process the pandoc output: convert mirrored figures to lossless WebP
and rewrite image paths/extensions in the generated Markdown.

Pandoc emits raw HTML <img src="..."> (not Markdown ![]()) for any LaTeX
figure with a caption/label, so the original sed-based path rewrite in
convert_thesis.sh never matched. This script handles both forms.

Run from the repo root after convert_thesis.sh has copied figures into
docs/assets/figures and generated docs/**/*.md.
"""

import os
import re
import subprocess
from pathlib import Path

DOCS = Path("docs")
FIGURES = DOCS / "assets" / "figures"


def convert_to_webp() -> None:
    images = [p for p in FIGURES.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg")]
    for src in images:
        dst = src.with_suffix(".webp")
        subprocess.run(["cwebp", "-quiet", "-lossless", str(src), "-o", str(dst)], check=True)
        src.unlink()
    print(f"Converted {len(images)} images to lossless WebP under {FIGURES}")


def rewrite_paths_in(md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    # docs/index.md sits one level shallower than docs/chapters/*.md, so the
    # relative path to assets/figures depends on where the file lives.
    prefix = Path(os.path.relpath(FIGURES, md_path.parent)).as_posix()

    def repl(match: re.Match) -> str:
        src = match.group("src")
        norm = re.sub(r"/+", "/", src)
        if "A1_figures/" in norm:
            new = f"{prefix}/A1/" + norm.split("A1_figures/", 1)[1]
        elif "A2_figures/" in norm:
            new = f"{prefix}/A2/" + norm.split("A2_figures/", 1)[1]
        elif "figures/" in norm:
            new = f"{prefix}/" + norm.split("figures/", 1)[1]
        else:
            return match.group(0)
        new = re.sub(r"\.(png|jpe?g)$", ".webp", new, flags=re.IGNORECASE)
        return match.group(0).replace(src, new)

    text = re.sub(r'src="(?P<src>[^"]+\.(?:png|jpe?g))"', repl, text, flags=re.IGNORECASE)
    text = re.sub(r"\]\((?P<src>[^)]+\.(?:png|jpe?g))\)", repl, text, flags=re.IGNORECASE)
    md_path.write_text(text, encoding="utf-8")


def main() -> None:
    convert_to_webp()
    for md_path in DOCS.rglob("*.md"):
        rewrite_paths_in(md_path)
    print("Rewrote image paths/extensions in generated Markdown")


if __name__ == "__main__":
    main()
