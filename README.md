# hesso-master-rooftops-latex

LaTeX template based on [hesso-latextemplate-thesis](https://github.com/mdemierre/hesso-latextemplate-thesis) for the HES-SO//Master MSE thesis in French.

## Thanks to

- Marc Demierre [@mdemierre](https://github.com/mdemierre) for the template
- Maria Sisto, for the title page
- Loïc Monney, for the section title style, captions style and font idea
- EPFL, for the basic structure

## Howto use it

- Install vscode and [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
- Install [latex](https://www.latex-project.org/get/#tex-distributions) for your OS
- Use this recipe in settings.json

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
