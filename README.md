# Technica

Technica is a small LaTeX style system for technical documents: tutorials,
course notes, reference material, engineering reports, and code-heavy articles.
It provides typography, semantic prose commands, code listings,
terminal sessions, and callouts behind one package entry point.

Load it with:

```latex
\usepackage{technica}
```

Global document styling is opt-in. By default, Technica provides code listings,
callouts, and prose macros while leaving fonts and document layout to the host.
Enable individual global styles, or use the full styling preset:

```latex
\usepackage[style=all]{technica}
```

XeLaTeX or LuaLaTeX is recommended for best font selection. pdfLaTeX is
supported with fallback fonts.

The supported document class is the standard `article` class. The compilation
suite also checks basic `report` and `book` documents: their title pages and
chapter headings stay under the class's control. With `layout=true`, Technica styles section-level
headings, but does not provide a chapter design. Other classes are untested;
leave `layout` disabled when the class should own the layout.

The document class or consuming document controls page format and title styling.
Technica does not load `geometry` or redefine `\maketitle`.

Select either built-in theme at package load time:

```latex
\usepackage[theme=dark]{technica} % default: light
```

The `pagecolors=true` switch applies the theme’s page background and body text
colors. By default, the consuming document owns those colors.
Use `pagecolors=true,theme=dark` to apply the dark theme to the whole document.

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

`\filepath`, `\command`, and `\api` read their arguments verbatim, preserving
backslashes, repeated hyphens, percent signs, and other literal characters.
Their monospace text uses the surrounding font size. For snippets containing a
closing brace, use matching delimiters that do not occur in the text:

```latex
\command{clang++ --version}
\filepath{C:\Users\ryan\file.txt}
\api!operator() { return value; }!
```

These three commands, and commands made with `\technicadefineinlinemacro`, must
appear directly in paragraph text on one source line. They cannot be nested in
arguments such as `\section{...}`, `\caption{...}`, or `\textbf{...}`; use ordinary
LaTeX text with escaping there. `\term` and `\key` remain ordinary prose commands.

Macro sets live in `macros/*.def`. Load a set on demand with
`\technicaloadmacroset`, then use the commands that definition provides:

```latex
\technicaloadmacroset{prose}
```

Definition names are trimmed, so spaces around entries in `sets` are allowed.
Loading is idempotent within the current scope. A set loaded inside a group is
local to that group and can be loaded again outside it.

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

Spaces around names in `languages` are allowed, for example `{cpp, sh}`. The
on-demand loader also trims names and follows the caller's scope: a language
loaded inside a group can be loaded again after the group ends.

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

Numbered blocks reserve an internal gutter sized for four digits in the active
number font. For wider labels, set `listingopts={technicanumberwidth={999999}}`;
the supplied text is measured to determine the gutter width. Unnumbered blocks
and inline code do not reserve a gutter.

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

Defining a color that was an alias replaces its binding with the supplied color.
For example, `\technicadefinecolor{TechnicaCodeBg}{FFFFFF}` gives code blocks an
independent white background. Rebinding an alias updates all of its dependent
aliases immediately, including chains of aliases. Alias targets must be named
colors; self-references and indirect cycles produce an error. Color definitions
and bindings follow normal TeX group scope.

## Configuration reference

The independent `fonts`, `headings`, `paragraphs`, `lists`, `captions`,
`pagecolors`, and `hyperlinks` switches default to `false`. A bare switch means
`true`. `style=all` enables all seven; explicit switches override the preset
regardless of option order. For example, both `style=all,fonts=false` and
`fonts=false,style=all` enable every global style except fonts.

`layout=true` is a shorthand for headings, paragraphs, lists, and captions;
individual switches override it too. Page colors and hyperlink styling require
their own opt-ins or `style=all`. Hyperlink styling configures an already loaded
`hyperref`; it does not load it. Enabled paragraphs are unindented and spaced
(`parindent=0pt`, `parskip=6pt plus 2pt minus 1pt`).

`code`, `boxes`, and `macros` still default to `true`. With `fonts=false`, the document is responsible for its fonts and font
encoding (for pdfLaTeX, normally `\usepackage[T1]{fontenc}`). Colors are loaded
by whichever enabled modules need them. Components use the document’s current
font families: code and literal prose use `\ttfamily`, callout titles and key
labels use `\sffamily`, and callout bodies inherit the surrounding family.

The top-level `theme` option defaults to `light`. Options for individual modules
are passed in braces through `fontopts`, `layoutopts`, `codeopts`, `boxopts`,
`macroopts`, and `coloropts`. `coloropts` currently accepts only `theme`; prefer
the top-level `theme` option instead of setting it in both places.
Module options do not enable a disabled module: `fontopts` requires `fonts=true`,
and `layoutopts` requires at least one layout style to be enabled.

### Fonts (`fontopts`)

| Option | Default / behavior |
| --- | --- |
| `mainfont` | Charter, if installed |
| `sansfont` | Avenir Next, with Demi Bold headings, if installed |
| `monofont` | Menlo, if installed |
| `mainfontscale` | `1.0` |
| `sansfontscale`, `monofontscale` | `MatchLowercase` |
| `mainfontfeatures`, `sansfontfeatures`, `monofontfeatures` | Empty; additional `fontspec` options |
| `kpfonts` | `false`; opt-in pdfLaTeX text/math fonts |
| `kpfontsopt` | Empty; options passed to `kpfonts` |

The default sans family maps bold and bold italic to Avenir Next Demi Bold
and Demi Bold Italic. An explicit `sansfont` uses that family's own weights;
`sansfontfeatures` can override the default face bindings.

Named fonts, scales, and features apply to XeLaTeX and LuaLaTeX. If a default
font is missing, Technica warns and the engine's existing font remains in use.
An explicitly requested missing font produces an error. pdfLaTeX uses T1 encoding and its
existing fonts unless `kpfonts=true` is supplied; it ignores named font options.

```latex
\usepackage[fonts=true,fontopts={mainfont={Libertinus Serif},monofontscale=0.9}]{technica}
```

### Layout (`layoutopts`)

| Option | Default / behavior |
| --- | --- |
| `parskip` | `6pt plus 2pt minus 1pt` |
| `parindent` | `0pt` |
| `titlespacing` | `true`; applies Technica's section spacing |
| `colorlinks` | `true`; chooses colored links when `hyperlinks=true` and `hyperref` is loaded |

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

A TeX installation with `listings`, `tcolorbox`, `titlesec`,
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

### Demo

Build the three-page sample in `examples/demo.tex`:

```sh
make demo                         # XeLaTeX
make demo ENGINE=pdflatex         # fallback fonts
```

The PDF is written to `output/pdf/technica-demo.pdf`. It demonstrates semantic
prose, C++ and generic code blocks, terminal sessions, callouts, and references.
Change `theme=light` to `theme=dark` in the source to preview the dark theme.

### Checks

```sh
make test                         # pdfLaTeX, XeLaTeX, and LuaLaTeX
make test ENGINES=pdflatex         # one engine
```

The tests require Python 3 and Poppler's `pdftotext`, plus the selected TeX
engines. Outputs and logs go into `build/tests/<engine>/<case>/`.

The checks compile actual documents and inspect PDF text for literal characters,
line numbers, selected source lines, and resolved references. They also exercise
module switches, retained title blocks, dark-theme callout text, basic class
compatibility, and code spanning pages. Regression cases also cover literal
prose, scoped definition loading, package load order, palette overrides and
alias chains, and C++ keyword recognition. Overfull boxes fail the checks.

Run `make install-hooks` to enable the pre-commit check requiring today's
`\ProvidesPackage` date in staged `.sty` files.
