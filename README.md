# Technica

Technica is a small LaTeX style system for technical documents: tutorials,
course notes, reference material, engineering reports, and code-heavy articles.
It provides a restrained page layout, semantic prose commands, code listings,
terminal sessions, and callouts behind one package entry point.

Load it with:

```latex
\usepackage{technica}
```

XeLaTeX or LuaLaTeX is recommended for best font selection. pdfLaTeX is
supported with fallback fonts.

The supported document class is the standard `article` class. The compilation
suite also checks basic `report` and `book` documents: their title pages and
chapter headings stay under the class's control. Technica styles section-level
headings, but does not provide a chapter design. Other classes are untested;
use `layout=false` when the class should own the layout.

To keep an article's existing title block while using the rest of Technica's
layout, pass `layoutopts={title=false}`. For non-article classes, title styling
is skipped with a warning; `title=false` suppresses that warning.

Select either built-in theme at package load time:

```latex
\usepackage[theme=dark]{technica} % default: light
```

The layout module applies the theme's page background and body text colors.
With `layout=false`, the consuming document owns those colors.

Technica defaults to a 7in by 10in page. Pass layout options through
`layoutopts`; use a named geometry paper size with `papersize`, or provide
custom dimensions with `paperwidth` and `paperheight`:

```latex
\usepackage[layoutopts={papersize=letterpaper}]{technica}
\usepackage[layoutopts={paperwidth=6in,paperheight=9in}]{technica}
```

Callout boxes are enabled by default. Disable them with `boxes=false`, or pass
box tuning options through `boxopts`:

```latex
\usepackage[boxopts={backmix=8,leftrule=4pt}]{technica}
```

Code blocks are enabled by default. Disable them with `code=false`, or choose
which language definitions to load through `codeopts`:

```latex
\usepackage[codeopts={languages={cpp,sh}}]{technica}
```

Semantic prose macros are enabled by default. Disable them with `macros=false`,
or choose which macro sets to load through `macroopts`:

```latex
\usepackage[macroopts={sets=prose}]{technica}
```

## API

### Semantic Prose

Use these commands to mark technical prose by meaning instead of presentation.
That keeps documents stable if the visual style changes later.

| Command | Use for | Example |
| --- | --- | --- |
| `\term{...}` | Important terms or first-use definitions | `\term{translation unit}` |
| `\filepath{...}` | File and directory paths | `\filepath{src/main.cpp}` |
| `\command{...}` | Command names or short invocations | `\command{clang++}` |
| `\api{...}` | APIs, types, functions, methods, endpoints | `\api{std::vector}` |
| `\key{...}` | Keyboard keys | `\key{Esc}` |

```latex
\term{Translation units} are compiled with \command{clang++}.
Open \filepath{src/main.cpp} and press \key{Esc}.
```

Macro sets live in `macros/*.def`. Load a set on demand with
`\technicaloadmacroset`, then use the commands that definition provides:

```latex
\technicaloadmacroset{prose}
```

New macro files should expose semantic wrappers through the Technica factories:

```latex
\technicadefineprosemacro{concept}{\bfseries\color{TechnicaInk}}{}
\technicadefineinlinemacro{configkey}
\technicadefinekeymacro{shortcut}
```

### Inline Code

Use inline code commands for short snippets inside paragraphs. Prefer these for
brief fragments and the block environments for anything multi-line.

| Command | Use for | Example |
| --- | --- | --- |
| `\inlinecode{...}` | Generic inline code | `\inlinecode{return value;}` |
| `\inlinecpp{...}` | Inline C++ | `\inlinecpp{std::vector<int>}` |
| `\inlinesh{...}` | Inline shell text | `\inlinesh{clang++ main.cpp}` |

```latex
Call \inlinecpp{std::vector<int>::push_back} from the loop.
Run \inlinesh{clang++ main.cpp} to build the example.
```

Pipes, percent signs, underscores, and other literal characters are supported
directly. Use a matching delimiter absent from the snippet when it contains
braces (including unmatched braces) or backslashes:

```latex
\inlinecpp{ready || retry}
\inlinecode{100% complete}
\inlinesh!printf '%s\n' "$HOME" | sort!
\inlinecpp!if (ready) { run(); }!
\inlinecode!C:\tmp\input.txt!
```

These commands let `listings` read the input verbatim. Keep them in ordinary
paragraph text, outside arguments to other commands such as `\section`,
`\caption`, or `\textbf`. Use ordinary LaTeX text with normal escaping in
headings and captions. Inline snippets must stay on one source
line. A literal closing brace requires the delimiter form.

### Code Blocks

#### `codeblock`

Generic titled code block.

```latex
\begin{codeblock}{config.txt}
name = technica
\end{codeblock}
```

#### `cpp`

C++ code block with a title, usually a filename.

```latex
\begin{cpp}{main.cpp}
int main() {
    return 0;
}
\end{cpp}
```

#### `terminal`

Terminal session block.

```latex
\begin{terminal}
$ clang++ main.cpp
$ ./a.out
\end{terminal}
```

Language-specific listings live in `languages/*.def`. Load a language on demand
with `\technicaloadcodelanguage`, then use the environments or inline commands
that definition provides:

```latex
\technicaloadcodelanguage{cpp}
\begin{cpp}{main.cpp}
int main() { return 0; }
\end{cpp}
```

New language files should define a listings style, then expose semantic wrappers
with `\technicadefinecodeblock` and `\technicadefineinlinecode`:

```latex
\lstdefinestyle{technica-python}{
    style=technica-base,
    language=Python
}
\technicadefinecodeblock{python}{technica-python}
\technicadefineinlinecode{inlinepython}{technica-python}
```

#### Per-block options and references

All block environments accept an optional `tcolorbox` settings argument before
the title. The `listingopts` key adds `listings` settings to the block's language
style. C++ blocks default to left-side line numbers; generic and terminal blocks
default to none.

```latex
\begin{cpp}[listingopts={numbers=left,firstnumber=20},label=code:parse]{parse.cpp}
int parse() { return 0; }
\end{cpp}

\begin{cpp}[listingopts={numbers=none}]{Short example}
return value;
\end{cpp}

\begin{terminal}[title={Build},listingopts={numbers=none}]
$ make
\end{terminal}

See block \ref{code:parse} on page \pageref{code:parse}.
```

Blocks share the `technicacode` counter, including terminal sessions and
environments created by `\technicadefinecodeblock`. Titles still display the
supplied text without a number. Compile twice to resolve references. Settings
are local to each block; put related listing settings in one `listingopts` value.

#### Include a source file

Use `\technicainputcode[options]{title}{path}` to include an existing file. Select
a loaded language style and, optionally, a line range:

```latex
\technicainputcode[
  listingopts={style=technica-cpp,firstline=10,lastline=25,firstnumber=10},
  label=code:source
]{parser.cpp}{src/parser.cpp}
```

The default style is language-neutral. Paths resolve through TeX's input search
path, normally relative to the compilation working directory.

### Callouts

Callout environments add labeled sidebars for common kinds of technical notes.
Choose the semantic environment that matches the role of the paragraph, not the
color you want.

| Environment | Use for |
| --- | --- |
| `note` | Neutral supporting information |
| `explanation` | Deeper explanation or mental model |
| `advice` | Recommendation or convention |
| `warning` | Risk, pitfall, or common mistake |

```latex
\begin{note}
Supporting information.
\end{note}

\begin{explanation}
A deeper explanation or mental model.
\end{explanation}

\begin{advice}
A recommendation or convention.
\end{advice}

\begin{warning}
A risk, pitfall, or common mistake.
\end{warning}
```

Define a domain-specific callout with `\technicadefinecallout`. The first
argument is the environment name, the second is the displayed label, and the
third is any `xcolor` color, including Technica palette colors:

```latex
\technicadefinecallout{tip}{Tip}{TechnicaAdvice}

\begin{tip}
A short recommendation specific to this document.
\end{tip}
```

### Colors

Technica colors are named `xcolor` colors. Redefine them after
`\usepackage{technica}` and before `\begin{document}`:

```latex
\technicadefinecolor{TechnicaMist}{F8FAF9}
\technicadefinecolor{TechnicaKeyword}{293BB5}
```

Some colors can alias others, so related surfaces stay together:

```latex
\technicaaliascolor{TechnicaCodeBg}{TechnicaMist}
```

Use `\technicadefinecolor` instead of raw `\definecolor` for Technica colors so
color aliases keep their recorded hex values in sync.

## Configuration reference

All five feature switches default to `true` and can be disabled independently:
`fonts`, `layout`, `code`, `boxes`, and `macros`. For example,
`\usepackage[fonts=false,boxes=false]{technica}` keeps layout, code, and prose
macros. With `fonts=false`, the document is responsible for its fonts and font
encoding (for pdfLaTeX, normally `\usepackage[T1]{fontenc}`). Colors are loaded
by whichever enabled modules need them.

The top-level `theme` option defaults to `light`. Options for individual modules
are passed in braces through `fontopts`, `layoutopts`, `codeopts`, `boxopts`,
`macroopts`, and `coloropts`. `coloropts` currently accepts only `theme`; prefer
the top-level `theme` option instead of setting it in both places.

### Fonts (`fontopts`)

| Option | Default / behavior |
| --- | --- |
| `mainfont` | Source Serif 4, if installed |
| `sansfont` | Source Sans 3, if installed |
| `monofont` | Source Code Pro, if installed |
| `mainfontscale` | `1.0` |
| `sansfontscale`, `monofontscale` | `MatchLowercase` |
| `mainfontfeatures`, `sansfontfeatures`, `monofontfeatures` | Empty; additional `fontspec` options |
| `kpfonts` | `false`; opt-in pdfLaTeX text/math fonts |
| `kpfontsopt` | Empty; options passed to `kpfonts` |

Named fonts, scales, and features apply to XeLaTeX and LuaLaTeX. If a default
font is missing, the engine's existing font remains in use. An explicitly
requested missing font produces an error. pdfLaTeX uses T1 encoding and its
existing fonts unless `kpfonts=true` is supplied; it ignores named font options.

```latex
\usepackage[fontopts={mainfont={Libertinus Serif},monofontscale=0.9}]{technica}
```

### Layout (`layoutopts`)

| Option | Default / behavior |
| --- | --- |
| `papersize` | Empty; named `geometry` size such as `a4paper`, overrides custom dimensions |
| `paperwidth`, `paperheight` | `7in`, `10in` |
| `margin` | `0.75in` |
| `headheight` | `14pt` |
| `parskip` | `6pt plus 2pt minus 1pt` |
| `parindent` | `0pt` |
| `titlespacing` | `true`; applies Technica's section spacing |
| `title` | `true`; applies the article title design |
| `colorlinks` | `true`; styles links if `hyperref` is loaded |

Technica does not load `hyperref`. Load it in the preamble to enable links;
Technica configures link colors at the start of the document. `titlespacing=false`
leaves section spacing to `titlesec`; it still applies heading typography.

### Code (`codeopts`) and callouts (`boxopts`)

| Option | Code default | Callout default |
| --- | --- | --- |
| `arc` | `3pt` | `3pt` |
| `left`, `right` | `8pt`, `8pt` | `10pt`, `12pt` |
| `top`, `bottom` | `8pt`, `8pt` | `8pt`, `8pt` |
| `beforeskip`, `afterskip` | `10pt plus 2pt minus 1pt` | `10pt plus 2pt minus 1pt` |
| `boxrule` | `0.6pt` | Not applicable |
| `languages` | `{cpp,sh}`; empty loads no language definitions | Not applicable |
| `leftrule` | Not applicable | `3pt` |
| `backmix`, `titlemix` | Not applicable | `6`, `6`; percentage of accent mixed into the page color |

### Prose macros (`macroopts`)

| Option | Default / behavior |
| --- | --- |
| `sets` | `prose`; empty loads no macro sets |
| `keypadding` | `1.25pt` |
| `keyrule` | `0.5pt` |

## Installation and development

A TeX installation with `listings`, `tcolorbox`, `geometry`, `titlesec`,
`caption`, `enumitem`, `microtype`, `xurl`, and their dependencies is required.
XeLaTeX and LuaLaTeX also use `fontspec`. No shell escape or external syntax
highlighter is needed.

From a consuming repository, point `TEXINPUTS` at this checkout:

```sh
TEXINPUTS=.:/path/to/technica//: xelatex chapters/example/example.tex
```

The initial `.` keeps generated listing files local to the compilation directory.
The trailing `//` includes definition subdirectories; the trailing `:` preserves
TeX's normal search path.

`make bundle` installs the package and definitions into
`$(TEXMFLOCAL)/tex/latex/technica` and runs `texhash` when available. It does not
create an archive. The default `TEXMFLOCAL` comes from `kpsewhich` and may require
system write permission. To install in your personal TeX tree instead:

```sh
make bundle TEXMFLOCAL="$(kpsewhich -var-value TEXMFHOME)"
```

### Checks and visual specimen

```sh
make test                         # pdfLaTeX, XeLaTeX, and LuaLaTeX
make test ENGINES=pdflatex         # one engine
make specimen                     # light + dark, using XeLaTeX
make specimen SPECIMEN_ENGINE=lualatex
```

These targets require Python 3 and Poppler's `pdftotext`, plus the selected TeX
engines. Outputs and logs go into `build/tests/<engine>/<case>/`. The specimen
PDFs are `specimen-light/specimen-light.pdf` and
`specimen-dark/specimen-dark.pdf` within the engine directory.

The checks compile actual documents and inspect PDF text for literal characters,
line numbers, selected source lines, and resolved references. They also exercise
module switches, retained title blocks, dark-theme callout text, basic class
compatibility, and code spanning pages. Both themes are compiled and overfull
boxes fail the checks.
Inspect the specimen PDFs when changing typography or spacing; compilation alone
cannot establish visual quality. Sources live in `examples/specimen.tex` and
`examples/sample.cpp`.

Run `make install-hooks` to enable the pre-commit check requiring today's
`\ProvidesPackage` date in staged `.sty` files.
