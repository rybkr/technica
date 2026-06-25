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
\usepackage[codeopts={languages={cxx,sh}}]{technica}
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
| `\inlinecxx{...}` | Inline C++ | `\inlinecxx{std::vector<int>}` |
| `\inlinesh{...}` | Inline shell text | `\inlinesh{clang++ main.cpp}` |

```latex
Call \inlinecxx{std::vector<int>::push_back} from the loop.
Run \inlinesh{clang++ main.cpp} to build the example.
```

### Code Blocks

#### `codeblock`

Generic titled code block.

```latex
\begin{codeblock}{config.txt}
name = technica
\end{codeblock}
```

#### `cxx`

C++ code block with a title, usually a filename.

```latex
\begin{cxx}{main.cpp}
int main() {
    return 0;
}
\end{cxx}
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
\technicaloadcodelanguage{cxx}
\begin{cxx}{main.cpp}
int main() { return 0; }
\end{cxx}
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
demo swatches and color aliases keep their recorded hex values in sync.

## Development Usage

From a consuming repository, point `TEXINPUTS` at this checkout:

```sh
TEXINPUTS=/path/to/technica//: xelatex chapters/example/example.tex
```

Build the local demo PDF with:

```sh
make demo.pdf
```
