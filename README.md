# hesso-master-rooftops-latex

LaTeX template based on [hesso-latextemplate-thesis](https://github.com/mdemierre/hesso-latextemplate-thesis) for the HES-SO//Master MSE thesis in French.

This repo contains two separate things — the LaTeX thesis itself, and the tooling that publishes it as a browsable website:

- **The LaTeX thesis**: `00-settings/`, `01-head/`, `02-main/`, `03-tail/`, `img/`, `thesis.tex`. Source of truth — see [LaTeX thesis](#latex-thesis) below.
- **The website**: generated *from* the LaTeX by `site-generator/`, built by MkDocs into `docs/`/`site/`. See [Documentation website (MkDocs)](#documentation-website-mkdocs) below.

## LaTeX thesis

- Install vscode and [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
- Install [latex](https://www.latex-project.org/get/#tex-distributions) for your OS
- Use this recipe in settings.json

<details>
<summary>VS Code <code>settings.json</code> recipe (click to expand)</summary>

```json
    "latex-workshop.latex.tools": [

        {
            "name": "latexmk",
            "command": "latexmk",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-pdf",
                "-outdir=%OUTDIR%",
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "lualatexmk",
            "command": "latexmk",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-lualatex",
                "-outdir=%OUTDIR%",
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "xelatexmk",
            "command": "latexmk",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-xelatex",
                "-outdir=%OUTDIR%",
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "latexmk_rconly",
            "command": "latexmk",
            "args": [
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "pdflatex",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "bibtex",
            "command": "bibtex",
            "args": [
                "%DOCFILE%"
            ],
            "env": {}
        },
        {
            "name": "rnw2tex",
            "command": "Rscript",
            "args": [
                "-e",
                "knitr::opts_knit$set(concordance = TRUE); knitr::knit('%DOCFILE_EXT%')"
            ],
            "env": {}
        },
        {
            "name": "jnw2tex",
            "command": "julia",
            "args": [
                "-e",
                "using Weave; weave(\"%DOC_EXT%\", doctype=\"tex\")"
            ],
            "env": {}
        },
        {
            "name": "jnw2texminted",
            "command": "julia",
            "args": [
                "-e",
                "using Weave; weave(\"%DOC_EXT%\", doctype=\"texminted\")"
            ],
            "env": {}
        },
        {
            "name": "pnw2tex",
            "command": "pweave",
            "args": [
                "-f",
                "tex",
                "%DOC_EXT%"
            ],
            "env": {}
        },
        {
            "name": "pnw2texminted",
            "command": "pweave",
            "args": [
                "-f",
                "texminted",
                "%DOC_EXT%"
            ],
            "env": {}
        },
        {
            "name": "tectonic",
            "command": "tectonic",
            "args": [
                "--synctex",
                "--keep-logs",
                "--print",
                "%DOC%.tex"
            ],
            "env": {}
        },
        {
            "name": "latexmk",
            "command": "latexmk",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-pdf",
                "-outdir=%OUTDIR%",
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "pdflatex",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "pdflatex_continue",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-shell-escape",
                "%DOC%"
            ],
            "env": {}
        },
        {
            "name": "biber",
            "command": "/Library/TeX/texbin/biber",
            "args": [
                "%DOCFILE%"
            ],
            "env": {}
        },
        {
            "name": "makeglossaries",
            "command": "/Library/TeX/texbin/makeglossaries",
            "args": [
                "%DOCFILE%"
            ],
            "env": {}
        },
        {
            "name": "bibtex",
            "command": "bibtex",
            "args": [
                "%DOCFILE%"
            ],
            "env": {}
        },
        {
            "name": "clean_aux",
            "command": "latexmk",
            "args": [
                "-c",
                "%DOC%"
            ],
            "env": {}
        },
                {
            "name": "latexmk_complete",
            "command": "latexmk",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-pdf",
                "-f",
                "-shell-escape",
                "-bibtex",
                "-outdir=%OUTDIR%",
                "%DOC%"
            ],
            "env": {}
        },
    ],
    "latex-workshop.latex.recipes": [

        {
            "name": "01_latexmk",
            "tools": [
                "latexmk_complete",
                "makeglossaries",
                "latexmk_complete"
            ]
        },

    ],
    "latex-workshop.latex.recipe.default": "01_latexmk",
    "latex-workshop.view.pdf.viewer": "tab",
    "latex-workshop.latex.build.forceRecipeUsage": false,
    "latex-workshop.message.error.show": true,
    "latex-workshop.message.warning.show": true,
    "latex-workshop.latex.watch.delay": 1000,
    "latex-workshop.latex.autoBuild.run": "never",
    "latex-workshop.showContextMenu": true,
    "latex-workshop.intellisense.package.enabled": true,
    "makefile.configureOnOpen": true,
    "latex-workshop.intellisense.bibtexJSON.replace": {},
    "editor.wordWrap": "on",
    "latex-utilities.liveReformat.snippets": [

        {
            "prefix": "([A-Za-z}\\)\\]])(\\d)$",
            "body": "$1_$2",
            "mode": "maths",
            "triggerWhenComplete": true,
            "description": "auto subscript"
        },
        {
            "prefix": "([A-Za-z}\\)\\]]) ?_(\\d\\d)$",
            "body": "$1_{$2}",
            "mode": "maths",
            "triggerWhenComplete": true,
            "description": "auto escape subscript"
        },
        {
            "prefix": "(\\S) ([\\^_])$",
            "body": "$1$2",
            "mode": "maths",
            "triggerWhenComplete": true,
            "description": "remove extraneous sub/superscript space",
            "priority": 2
        },
        {
            "prefix": "([A-Za-z}\\)\\]]) ?\\^ ?(\\d\\d|[\\+\\-] ?(?:\\d|[A-Za-z]|\\\\\\w+))$",
            "body": "$1^{$2}",
            "mode": "maths",
            "triggerWhenComplete": true,
            "description": "auto escape superscript",
            "priority": 2
        },
        {
            "prefix": "([^ &\\\\\\+\\-=<>\\|!~@])([\\+\\-=<>])$",
            "body": "$1 $2",
            "mode": "maths",
            "priority": -1,
            "description": "whitespace before operators",
            "triggerWhenComplete": true
        },
        {
            "prefix": "([\\+\\-=<>])([^ &\\\\\\+\\-=<>\\|!~])$",
            "body": "$1 $2",
            "mode": "maths",
            "priority": -1,
            "description": "whitespace after operators",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\.\\.\\.$",
            "body": "\\dots ",
            "mode": "maths",
            "description": "⋯",
            "triggerWhenComplete": true
        },
        {
            "prefix": "=>$",
            "body": "\\implies ",
            "mode": "maths",
            "description": "⇒",
            "triggerWhenComplete": true
        },
        {
            "prefix": "=<$",
            "body": "\\impliedby ",
            "mode": "maths",
            "description": "implied by",
            "triggerWhenComplete": true
        },
        {
            "prefix": "//$",
            "body": "\\frac{$$1}{$$2} ",
            "mode": "maths",
            "description": "fraction (empty)",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(([\\d\\.]+)|([\\d\\.]*)(\\\\)?([A-Za-z]+)((\\^|_)(\\{\\d+\\}|\\d|[A-Za-z]|\\\\\\w+))*!?)\\/$",
            "body": "\\frac{$1}{$$1}$$0",
            "mode": "maths",
            "description": "fraction (from regex)",
            "triggerWhenComplete": true
        },
        {
            "prefix": "([\\)\\]}]) ?/$",
            "body": "SPECIAL_ACTION_FRACTION",
            "mode": "maths",
            "description": "fraction (parsed)",
            "triggerWhenComplete": true,
            "noPlaceholders": false
        },
        {
            "prefix": "sympy$",
            "body": "sympy $$1 sympy",
            "mode": "maths",
            "description": "sympy block",
            "triggerWhenComplete": false
        },
        {
            "prefix": "sympy.+$",
            "body": "SPECIAL_ACTION_BREAK",
            "mode": "maths",
            "triggerWhenComplete": true,
            "priority": 2
        },
        {
            "prefix": "sympy ?(.+?) ?sympy ?$",
            "body": "SPECIAL_ACTION_SYMPY",
            "mode": "maths",
            "priority": 3,
            "description": "sympy",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])\\biff$",
            "body": "$1\\iff ",
            "mode": "maths",
            "description": "⇔",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])\\binn$",
            "body": "$1\\in ",
            "mode": "maths",
            "description": "in",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])\\bnotin$",
            "body": "$1\\not\\in ",
            "mode": "maths",
            "description": "∈",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?!=$",
            "body": " \\neq ",
            "mode": "maths",
            "description": "neq",
            "triggerWhenComplete": true
        },
        {
            "prefix": "==$",
            "body": "&= ",
            "mode": "maths",
            "description": "aligned equal",
            "priority": 1,
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?~=$",
            "body": " \\approx ",
            "mode": "maths",
            "description": "≈",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?~~$",
            "body": " \\sim ",
            "mode": "maths",
            "description": "∼",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?>=$",
            "body": " \\geq ",
            "mode": "maths",
            "description": "≥",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?<=$",
            "body": " \\leq ",
            "mode": "maths",
            "description": "≤",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?>>$",
            "body": " \\gg ",
            "mode": "maths",
            "description": "≫",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?<<$",
            "body": " \\ll ",
            "mode": "maths",
            "description": "≪",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?xx$",
            "body": " \\times ",
            "mode": "maths",
            "description": "×",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?\\*\\*$",
            "body": " \\cdot ",
            "mode": "maths",
            "description": "⋅",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\]\\b|[ ,\\)\\]\\}]\\w*)(to|->)$",
            "body": "$1\\to ",
            "mode": "maths",
            "description": "→",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?(?:\\|->|!>)$",
            "body": " \\mapsto ",
            "mode": "maths",
            "description": "↦",
            "priority": 1.1,
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])a(?:rc)?(sin|cos|tan|cot|csc|sec)$",
            "body": "$1\\arc$2 ",
            "mode": "maths",
            "description": "arc(trig)",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])(sin|cos|tan|cot|csc|sec|min|max|log|exp)$",
            "body": "$1\\$2 ",
            "mode": "maths",
            "description": "un-backslashed operator",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])(pi)$",
            "body": "$1\\$2",
            "mode": "maths",
            "description": "pi",
            "triggerWhenComplete": true
        },
        {
            "prefix": "((?:\\b|\\\\)\\w{1,7})(,\\.|\\.,)$",
            "body": "\\vec{$1}",
            "mode": "maths",
            "description": "vector",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(\\\\?[\\w\\^]{1,7})~ $",
            "body": "\\tilde{$1}",
            "mode": "maths",
            "description": "tilde",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(\\\\?[\\w\\^]{1,7})\\. $",
            "body": "\\dot{$1}",
            "mode": "maths",
            "description": "dot",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(\\\\?[\\w\\^]{1,7})\\.\\. $",
            "body": "\\ddot{$1}",
            "mode": "maths",
            "description": "ddot",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bbar$",
            "body": "\\overline{$$1}",
            "mode": "maths",
            "description": "overline",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\b(\\\\?[\\w\\^{}]{1,3})bar$",
            "body": "\\overline{$1}",
            "mode": "maths",
            "description": "overline",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])\\bhat$",
            "body": "$1\\hat{$$1}",
            "mode": "maths",
            "description": "hat",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\b([\\w\\^{}])hat$",
            "body": "\\hat{$1}",
            "mode": "maths",
            "description": "hat",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\\\\\)(\\w)$",
            "body": "\\) $1",
            "mode": "any",
            "description": "space after inline maths",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\\\\\\\\\\\$",
            "body": "\\setminus ",
            "mode": "maths",
            "description": "∖ (setminus)",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bpmat$",
            "body": "\\begin{pmatrix} $$1 \\end{pmatrix} ",
            "mode": "maths",
            "description": "pmatrix",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bbmat$",
            "body": "\\begin{bmatrix} $$1 \\end{bmatrix} ",
            "mode": "maths",
            "description": "bmatrix",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bpart$",
            "body": "\\frac{\\partial $${1:V}}{\\partial $${2:x}} ",
            "mode": "maths",
            "description": "partial derivative",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bsq$",
            "body": "\\sqrt{$$1}",
            "mode": "maths",
            "description": "√",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?sr$",
            "body": "^2",
            "mode": "maths",
            "description": "²",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?cb$",
            "body": "^3",
            "mode": "maths",
            "description": "³",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bEE$",
            "body": "\\exists ",
            "mode": "maths",
            "description": "∃",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bAA$",
            "body": "\\forall ",
            "mode": "maths",
            "description": "∀",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\b([A-Za-z])([A-Za-z])\\2$",
            "body": "$1_$2",
            "mode": "maths",
            "description": "subscript letter",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\b([A-Za-z])([A-Za-z])\\2?p1$",
            "body": "$1_{$2+1}",
            "mode": "maths",
            "description": "subscript letter + 1",
            "priority": 2,
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bdint$",
            "body": "\\int_{$${1:-\\infty}}^{$${2:\\infty}} ",
            "mode": "maths",
            "description": "∫ₐᵇ",
            "triggerWhenComplete": true
        },
        {
            "prefix": "([^ \\\\])  $",
            "body": "$1\\, ",
            "mode": "maths",
            "description": "add maths whitespace \\,",
            "priority": -1,
            "triggerWhenComplete": true
        },
        {
            "prefix": "([^ \\\\])\\\\, {2,4}$",
            "body": "$1\\: ",
            "mode": "maths",
            "description": "add maths whitespace \\:",
            "priority": 0.1,
            "triggerWhenComplete": true
        },
        {
            "prefix": "([^ \\\\])\\\\: {2,4}$",
            "body": "$1\\; ",
            "mode": "maths",
            "description": "add maths whitespace \\;",
            "priority": 0.2,
            "triggerWhenComplete": true
        },
        {
            "prefix": "([^ \\\\])\\\\; {2,4}$",
            "body": "$1\\ ",
            "mode": "maths",
            "description": "add maths whitespace \\ ",
            "priority": 0.3,
            "triggerWhenComplete": true
        },
        {
            "prefix": "([^ \\\\])\\\\ {2,4}$",
            "body": "$1\\quad ",
            "mode": "maths",
            "description": "add maths whitespace quad",
            "priority": 0.4,
            "triggerWhenComplete": true
        },
        {
            "prefix": "([^ \\\\])\\\\quad {2,4}$",
            "body": "$1\\qquad ",
            "mode": "maths",
            "description": "add maths whitespace qquad",
            "priority": 0.5,
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bset$",
            "body": "\\\\{$$1\\\\} ",
            "mode": "maths",
            "description": "set {}",
            "triggerWhenComplete": true
        },
        {
            "prefix": " ?\\|\\|$",
            "body": " \\mid ",
            "mode": "maths",
            "description": "∣",
            "triggerWhenComplete": true
        },
        {
            "prefix": "< ?>$",
            "body": "\\diamond ",
            "mode": "maths",
            "description": "⋄",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\bcase$",
            "body": "\\begin{cases} $$1 \\end{cases} ",
            "mode": "maths",
            "description": "cases",
            "triggerWhenComplete": true
        },
        {
            "prefix": "(^|[^\\\\])\\bst$",
            "body": "$1\\text{s.t.} ",
            "mode": "maths",
            "description": "such that",
            "triggerWhenComplete": true
        },
        {
            "prefix": "\\+ ?-$",
            "body": "\\pm ",
            "mode": "maths",
            "description": "±",
            "priority": 1,
            "triggerWhenComplete": true
        },
        {
            "prefix": "- ?\\+$",
            "body": "\\mp ",
            "mode": "maths",
            "description": "∓",
            "priority": 1,
            "triggerWhenComplete": true
        },
        {
            "prefix": "(?:([A-Za-z0-9]|\\\\\\w{,7})|\\(([^\\)]+)\\))C(?:([A-Za-z0-9]|\\\\\\w{,7})|\\(([^\\)]+)\\))$",
            "body": "\\binom{$1$2}{$3$4}",
            "mode": "maths",
            "priority": 2,
            "description": "binomial",
            "triggerWhenComplete": true
        }
    ],
```

</details>

## Documentation website (MkDocs)

The thesis is also published as a browsable website (MkDocs Material), generated from the LaTeX above by the scripts in `site-generator/`:

- `site-generator/` — the scripts that convert the LaTeX into the website (`convert_thesis.sh` and everything it calls). Not LaTeX, not website content — just the tooling in between.
- `docs/` — the generated website content that MkDocs builds from. It is **generated from the LaTeX sources** — never edit files under `docs/chapters/`, `docs/appendices/`, `docs/bibliography.md`, `docs/glossary.md`, or `docs/assets/` by hand, since the next regeneration overwrites them. The only hand-written content is `docs/index.md` (the landing page) and `docs/img/` (favicon + social-preview image, used for Open Graph/Twitter link previews).
- `mkdocs.yml` — MkDocs site configuration (theme, nav, plugins). Stays at the repo root since that's where `mkdocs` expects to find it.
- `overrides/main.html` — injects Open Graph/Twitter Card meta tags (title, description, `docs/img/social-card.png`) into every page's `<head>`, so sharing a link on LinkedIn/Twitter/etc. shows a proper preview card instead of nothing.

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package/venv manager)
- [pandoc](https://pandoc.org/installing.html) (LaTeX → Markdown conversion + bibliography processing)
- [cwebp](https://developers.google.com/speed/webp/download) (image conversion to WebP) — on macOS: `brew install webp`

Install the Python dependencies (MkDocs Material) once with:

```bash
uv sync
```

### Regenerate the site from the LaTeX sources

Run from the repo root:

```bash
./site-generator/convert_thesis.sh
```

This single script does everything:

1. Mirrors figure folders into `docs/assets/figures/` and converts every image to lossless WebP ([fix_images.py](site-generator/fix_images.py)).
2. Converts the abstract/résumé ([01-head/05_abstracts.tex](01-head/05_abstracts.tex)) to its own chapter page (`docs/chapters/00-resume.md`).
3. Concatenates the 5 chapters + 2 appendices and runs them through **one** pandoc + citeproc pass, so figure/table/equation numbers and the bibliography are globally consistent (matching the original LaTeX, which is one continuous document) — then splits the result back into the per-chapter files MkDocs needs, plus a standalone `docs/bibliography.md` ([split_combined.py](site-generator/split_combined.py)).
4. Fixes up cross-references, math rendering, custom code/table environments pandoc can't parse natively, and citation links ([fix_text.py](site-generator/fix_text.py)).
5. Converts `03-tail/glossary.tex` to `docs/glossary.md` and resolves any citations inside glossary entries ([glossary_to_md.py](site-generator/glossary_to_md.py)).
6. Links every acronym/glossary-term usage across the site to its glossary entry ([link_glossary.py](site-generator/link_glossary.py)).

None of this touches the original `.tex` sources or images — all LaTeX constructs pandoc can't parse natively are patched on throwaway copies first ([preprocess_tex.py](site-generator/preprocess_tex.py)).

### Preview locally

```bash
uv run mkdocs serve
```

Then open <http://127.0.0.1:8000>. `mkdocs serve` watches `docs/` and `mkdocs.yml` and reloads automatically — but it does **not** re-run the LaTeX conversion, so re-run `convert_thesis.sh` first after editing any chapter/appendix `.tex` file.

### Build the static site

```bash
uv run mkdocs build --strict
```

Outputs to `site/`. `--strict` turns any broken internal link or missing file into a build failure — always run this after regenerating before committing, since it's the fastest way to catch a broken cross-reference.

### Publishing

[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) deploys `docs/` to GitHub Pages on every push to `main` — it only runs `mkdocs gh-deploy`, it does **not** regenerate `docs/` from the LaTeX sources. Always run `convert_thesis.sh` and commit the resulting `docs/` changes yourself before pushing.

### Linting the build scripts

The `site-generator/*.py` scripts and `convert_thesis.sh` are linted with [ruff](https://docs.astral.sh/ruff/) and [shellcheck](https://www.shellcheck.net/):

```bash
uv run ruff check --fix .   # lint + autofix
uv run ruff format .        # format
brew install shellcheck     # one-time, macOS
shellcheck site-generator/convert_thesis.sh
```

A [pre-commit](https://pre-commit.com/) hook runs both automatically on every commit. One-time setup:

```bash
brew install pre-commit shellcheck   # macOS
pre-commit install
```

## Thanks to

- Marc Demierre [@mdemierre](https://github.com/mdemierre) for the template
- Maria Sisto, for the title page
- Loïc Monney, for the section title style, captions style and font idea
- EPFL, for the basic structure
