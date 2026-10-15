# Technica

Technica is a small LaTeX style system for technical documents: tutorials,
course notes, reference material, engineering reports, and code-heavy articles.
It provides typography, semantic prose commands, code listings, terminal sessions,
and callouts behind one package entry point.

By default, `\usepackage{technica}` enables code, callouts, and prose macros while
leaving fonts and document layout to the host. Global styling is opt-in: enable
individual features or use `style=all` for the full preset.

## Installation

A TeX installation with `listings`, `tcolorbox`, `titlesec`, `caption`, `enumitem`,
`microtype`, `xurl`, and their dependencies is required. XeLaTeX and LuaLaTeX also
use `fontspec`. No shell escape or external syntax highlighter is needed.

From a consuming repository, point `TEXINPUTS` at this checkout:

```sh
TEXINPUTS=.:/path/to/technica//: xelatex example.tex
```

The initial `.` keeps generated listing files local to the compilation directory.
The trailing `//` includes definition subdirectories; the trailing `:` preserves
TeX's normal search path.

Alternatively, install into your personal TeX tree:

```sh
make bundle TEXMFLOCAL="$(kpsewhich -var-value TEXMFHOME)"
```

`make bundle` installs into `$(TEXMFLOCAL)/tex/latex/technica` and runs `texhash`
when available; it does not create an archive. Without the override above,
`TEXMFLOCAL` comes from `kpsewhich` and may require system write permission.

## Quick start

Save this as `example.tex` and compile with XeLaTeX or LuaLaTeX for best font
selection. pdfLaTeX is also supported with fallback fonts.

```latex
\documentclass{article}
\usepackage[style=all]{technica}
\usepackage{hyperref}

\begin{document}
\section{A small example}
A \term{translation unit} is compiled with \command{clang++}.
Open \filepath{src/main.cpp} and press \key{Esc}.

\begin{cpp}{main.cpp}
int main() {
    return 0;
}
\end{cpp}

\begin{note}
Compile twice when using references.
\end{note}
\end{document}
```

Technica does not load `hyperref`; load it yourself when using hyperlinks.
The `hyperlinks` switch, included in `style=all`, styles an already loaded
`hyperref` package.

The supported class is standard `article`. Basic `report` and `book` documents
are also tested, but their chapter headings remain under the class's control.
Other classes are untested. Leave global styling disabled when the class should
own it. Technica does not load `geometry` or redefine `\maketitle`; page format
and title design belong to the consuming document.

## Writing with Technica

| Feature | Commands or environments |
| --- | --- |
| Semantic prose | `\term`, `\filepath`, `\command`, `\api`, `\key` |
| Inline code | `\inlinecode`, `\inlinecpp`, `\inlinesh` |
| Titled code blocks | `\begin{codeblock}{Title}`, `\begin{cpp}{main.cpp}` |
| Terminal sessions | `\begin{terminal}` |
| Callouts | `note`, `explanation`, `advice`, `warning` |

C++ blocks have line numbers by default; generic blocks and terminal sessions
have none. Blocks support local listing options, labels, and source-file input.
See the [API reference](docs/reference.md#api) for examples and extension factories.

`\filepath`, `\command`, `\api`, and the inline-code commands read verbatim text.
Keep each use on one source line, directly in paragraph text—not inside
`\section`, `\caption`, `\textbf`, or other command arguments. Use a delimiter
absent from the text when it contains a closing brace:

```latex
\inlinecpp!if (ready) { run(); }!
```

`\term` and `\key` are ordinary prose commands.

## Configuration

The independent `fonts`, `headings`, `paragraphs`, `lists`, `captions`,
`pagecolors`, and `hyperlinks` switches default to `false`. `style=all` enables
all seven; explicit switches override the preset. `layout=true` enables only
headings, paragraphs, lists, and captions.

```latex
\usepackage[style=all,fonts=false]{technica} % keep the host's fonts
\usepackage[pagecolors=true,theme=dark]{technica} % dark page and components
```

These are alternative package declarations. The default theme is `light`;
`theme=dark` alone changes component colors without changing the page colors.
With fonts disabled, the host also owns font encoding (normally
`\usepackage[T1]{fontenc}` for pdfLaTeX).

Disable components with `code=false`, `boxes=false`, or `macros=false`. Pass
module options through `fontopts`, `layoutopts`, `codeopts`, `boxopts`,
`macroopts`, and `coloropts`, or select a reusable file with
`config={styles/course.cfg}`.

See the [configuration reference](docs/reference.md#configuration-reference)
for defaults and option tables, and
[named configuration files](docs/reference.md#named-configuration-files) for
merging rules and deferred definitions.

## Demo and development

View the [demo PDF](output/pdf/technica-demo.pdf) or build it from
[examples/demo.tex](examples/demo.tex) with `make demo`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the source layout, demo build options,
regression checks, and commit hooks.
