#!/usr/bin/env bash
# Converts the LaTeX thesis (hesso-master-rooftops-latex) to Markdown for MkDocs Material.
# Run from the repo root: ./convert_thesis.sh
#
# docs/index.md is hand-written (a short landing page, not the abstract) and
# is never touched by this script or by glossary_to_md.py/link_glossary.py's
# own writes — don't delete it when clearing docs/ before a regen.
set -euo pipefail

DOCS="docs"
BIB="03-tail/bibliography.bib"

mkdir -p "$DOCS/chapters" "$DOCS/appendices" \
         "$DOCS/assets/figures/A1" "$DOCS/assets/figures/A2"

# Mirror figure trees once so converted Markdown can use simple relative paths.
cp -r 02-main/figures/. "$DOCS/assets/figures/"
cp -r 03-tail/A1_fondamentaux_ML/A1_figures/. "$DOCS/assets/figures/A1/"
cp -r 03-tail/A2_fondamentaux_energie/A2_figures/. "$DOCS/assets/figures/A2/"

SCRIPT_DIR="$(dirname "$0")"
CSL="$SCRIPT_DIR/numeric-citation-order.csl"
PANDOC_TO="markdown_strict+pipe_tables+yaml_metadata_block+header_attributes+raw_html+link_attributes+fenced_divs+footnotes"

# pandoc's LaTeX table reader silently drops an entire \begin{table} block (no
# warning) if its tabular is wrapped in \makebox[\textwidth][c]{...} or uses
# \multicolumn. preprocess_tex.py strips those from a throwaway temp copy so
# the original .tex sources are never touched.
preprocess() {
  local src="$1"
  local tmp
  tmp="$(mktemp -t thesis_preproc)"
  uv run python3 "$SCRIPT_DIR/preprocess_tex.py" "$src" "$tmp"
  echo "$tmp"
}

# The abstract/résumé gets its own chapter page (not the landing page —
# docs/index.md is a hand-written summary, see below) with its own small set
# of citations, kept as its own pandoc+citeproc run.
tmp="$(preprocess 01-head/05_abstracts.tex)"
pandoc "$tmp" -o "$DOCS/chapters/00-resume.md" \
  --from=latex --to="$PANDOC_TO" \
  --bibliography="$BIB" --citeproc --csl="$CSL" \
  --metadata link-citations=true --metadata reference-section-title=Bibliographie \
  --wrap=none --mathjax
rm -f "$tmp"
echo "Converted: 01-head/05_abstracts.tex -> $DOCS/chapters/00-resume.md"

# The 5 chapters + 2 appendices are concatenated and run through ONE
# pandoc+citeproc pass, so citation numbers and the bibliography are globally
# consistent (matching the original LaTeX, which is one continuous compile)
# instead of each chapter restarting its own numbering and printing its own
# copy of the reference list.
BODY_SOURCES=(
  "02-main/ch1_introduction.tex"
  "02-main/ch2_analysis.tex"
  "02-main/ch3_modele.tex"
  "02-main/ch4_implementation.tex"
  "02-main/ch5_conclusions.tex"
  "03-tail/A1_fondamentaux_ML/A1_fondamentaux_ml.tex"
  "03-tail/A2_fondamentaux_energie/A2_fondamentaux_en.tex"
)
BODY_OUTPUTS=(
  "$DOCS/chapters/01-introduction.md"
  "$DOCS/chapters/02-analysis.md"
  "$DOCS/chapters/03-modele.md"
  "$DOCS/chapters/04-implementation.md"
  "$DOCS/chapters/05-conclusions.md"
  "$DOCS/appendices/A1-fondamentaux-ml.md"
  "$DOCS/appendices/A2-fondamentaux-energie.md"
)

COMBINED_SRC="$(mktemp -t thesis_combined_src)"
: > "$COMBINED_SRC"
for src in "${BODY_SOURCES[@]}"; do
  tmp="$(preprocess "$src")"
  cat "$tmp" >> "$COMBINED_SRC"
  echo "" >> "$COMBINED_SRC"
  rm -f "$tmp"
done

# glossary.tex uses package-specific commands (\newglossaryentry, \newacronym)
# pandoc can't parse, so it's converted separately by glossary_to_md.py — but
# a few glossary entries cite sources that are *only* cited there, never in
# the chapters. Append a throwaway paragraph citing them too so this same
# citeproc pass numbers and lists them in the shared bibliography; the
# GLOSSARYCITEPLACEHOLDER marker lets split_combined.py delete the paragraph
# afterwards (the citations themselves stay, now resolved).
GLOSSARY_TEX="03-tail/glossary.tex"
GLOSSARY_CITE_KEYS="$(grep -oh '\\cite{[^}]*}' "$GLOSSARY_TEX" | sed -E 's/\\cite\{(.*)\}/\1/' | tr ',' '\n' | sort -u)"
MARKER_CITES=""
for key in $GLOSSARY_CITE_KEYS; do
  if ! grep -q "cite{[^}]*\b${key}\b[^}]*}" "$COMBINED_SRC"; then
    MARKER_CITES="$MARKER_CITES \\cite{$key}"
  fi
done
if [ -n "$MARKER_CITES" ]; then
  printf '\nGLOSSARYCITEPLACEHOLDER%s\n' "$MARKER_CITES" >> "$COMBINED_SRC"
fi

COMBINED_OUT="$(mktemp -t thesis_combined_out)"
pandoc "$COMBINED_SRC" -o "$COMBINED_OUT" \
  --from=latex --to="$PANDOC_TO" \
  --bibliography="$BIB" --citeproc --csl="$CSL" \
  --metadata link-citations=true --metadata reference-section-title=Bibliographie \
  --wrap=none --mathjax
rm -f "$COMBINED_SRC"

uv run python3 "$SCRIPT_DIR/split_combined.py" "$COMBINED_OUT" Bibliographie "${BODY_OUTPUTS[@]}"
rm -f "$COMBINED_OUT"
for src in "${BODY_SOURCES[@]}"; do
  echo "Converted: $src -> (combined pass)"
done
echo "Wrote shared bibliography: $DOCS/bibliography.md"

# Pandoc keeps the original \includegraphics path (e.g. figures/ch2/x.png) and
# emits it as raw HTML <img src="..."> for any captioned figure. Convert the
# mirrored copies to lossless WebP and rewrite every image reference to match.
uv run python3 "$SCRIPT_DIR/fix_images.py"

# Fix up math escaping pandoc introduces when it falls back to raw TeX, and
# resolve figure/table/equation/section cross-references to clickable numbers
# instead of the raw \ref{} labels pandoc leaves behind.
uv run python3 "$SCRIPT_DIR/fix_text.py"

# glossary.tex uses package-specific commands pandoc can't parse, so it's
# converted separately here — after bibliography.md exists, since glossary
# descriptions cite sources that need resolving to the same numbered links.
uv run python3 "$SCRIPT_DIR/glossary_to_md.py"

# Every \gls{}/\acrshort{}/\acrlong{} usage across the site is currently a
# bare, unlinked span. Point each one at its entry on the glossary page.
uv run python3 "$SCRIPT_DIR/link_glossary.py"

echo
echo "Done."
