# Technica reference

See the [README](../README.md) for installation and a minimal document, or
[CONTRIBUTING.md](../CONTRIBUTING.md) for development instructions.

- [API](#api): prose, inline code, code blocks, callouts, and colors
- [Named configuration files](#named-configuration-files)
- [Configuration reference](#configuration-reference)

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

Terminal session block. A command line starts with `❯` followed by a literal
space in the first column. The prompt uses `TechnicaPrompt`; the entire command
(including arguments, operators, and arbitrary program names) uses
`TechnicaCommand`. All other lines use `TechnicaInk`, without keyword matching.
Wrapped command lines retain their input color. Indented markers, bare markers,
and markers within output do not start commands.

```latex
\begin{terminal}
❯ clang++ main.cpp
❯ ./a.out
\end{terminal}
```

Set `terminalprompt` in `listingopts` to change the marker for a block. Use
`❯` or a nonempty printable ASCII marker without spaces; the required separating
space is added by the matcher, so do not include it in the option:

```latex
\begin{terminal}[listingopts={terminalprompt={>>>}}]
>>> ps
PID TTY TIME CMD
6191 ttys001 0:00.00 ps
\end{terminal}
```

`terminalprompt={$}` supports traditional transcripts. This is a source-line
convention, not a shell parser: output beginning with the configured marker and
a space is also treated as input. Choose another marker if output would collide.
Continuation lines need their own prompt to receive input coloring. Existing
`$ ` transcripts must change to `❯ ` or select `terminalprompt={$}`.
`\inlinesh` colors its entire contents as input without requiring a prompt.
The default chevron is drawn independently of the document font on all engines.
It is omitted from copied PDF text; choose an ASCII marker if copied prompts
are needed.

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
❯ make
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

Select a built-in theme with `theme=light` (the default) or `theme=dark`.
Themes apply to components; add `pagecolors=true` to apply the theme to the
page background and body text too.

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

## Named configuration files

Select a reusable configuration explicitly at package load time:

```latex
\usepackage[config={styles/course.cfg}]{technica}
```

The file uses ordinary LaTeX syntax and the same keys as package options:

```latex
% styles/course.cfg
\technicasetup{
    fonts=true,
    layout=true,
    theme=light,
    fontopts={monofontscale=0.9},
    layoutopts={parskip={6pt plus 2pt minus 1pt}},
    codeopts={languages={cpp,sh},arc=3pt},
    boxopts={leftrule=3pt},
    macroopts={sets=prose}
}

\technicaaftersetup{
    \technicadefinecallout{designrule}{Design rule}{TechnicaExplanation}
    \technicadefineinlinemacro{configkey}
}
```

Technica reads the file before loading its modules. `\technicasetup` collects
settings; `\technicaaftersetup` defers definitions until all enabled modules
have loaded, before `\usepackage{technica}` returns. Enable the modules needed
by those definitions. Both commands may occur multiple times in the file;
settings merge and deferred blocks execute in declaration order. These commands
are only available for configuration during this loading phase, not for later
reconfiguration in the document.

Built-in defaults are overridden by file settings, then by explicit package
options, regardless of where `config` occurs in the option list:

```latex
\usepackage[codeopts={arc=0pt},config={styles/course.cfg},fonts=false]{technica}
```

Module option lists merge by key: this overrides `arc` while keeping the file's
`languages`. List values themselves are replaced: `languages={sh}` selects only
shell definitions, and `languages={}` loads none. Likewise, `sets={}` disables
loading macro sets. An empty outer option list such as `codeopts={}` contributes
no overrides. Repeated settings use their last value within each layer.

After merging, `style=all` and `layout=true` resolve as usual: explicit individual
feature switches beat these presets, including switches supplied by the file.
Module options do not enable disabled modules. The top-level `theme` remains
authoritative over `coloropts={theme=...}`; prefer the top-level key consistently.

There is no automatic configuration discovery. Supply one filename, including
its extension; paths use TeX's normal input search path, normally relative to
the compilation working directory, not necessarily the document directory.
A missing requested file, unknown top-level key, or unknown option for an enabled
module produces an error. Nested `config` selection is not supported. Without
`config`, existing package usage continues to work.

Configuration files are TeX source. Keep page geometry, title design, and document
metadata in the consuming document. See [examples/course.cfg](../examples/course.cfg) for a reusable
starting point.

## Configuration reference

The independent `fonts`, `title`, `toc`, `headings`, `paragraphs`, `lists`, `captions`,
`pagecolors`, and `hyperlinks` switches default to `false`. A bare switch means
`true`. `style=all` enables all nine; explicit switches override the preset
regardless of option order. For example, both `style=all,fonts=false` and
`fonts=false,style=all` enable every global style except fonts.

`layout=true` is a shorthand for headings, paragraphs, lists, and captions;
individual switches override it too. Title, TOC, page colors, and hyperlink styling require
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

### Table of contents (`toc`)

`toc=true` enables TOC styling through `tocloft`; it is also included in
`style=all`, but not `layout=true`. Use `toc=false` to retain host TOC styling.
The Contents title uses Technica's unnumbered section typography and spacing,
independently of `headings`. Section entries and page numbers use bold heading
text, with extra space between sections. Subsections use regular body text and
retain the class's indentation. Page numbers are right-aligned with muted dot
leaders. Chapter entries in `report` and `book` use the heading font.

The document still calls `\tableofcontents` and controls `\contentsname`,
`tocdepth`, numbering, and placement. When `hyperref` is loaded, entries and page
numbers are clickable without link coloring or borders; this setting is local
to the TOC. Technica does not load `hyperref`. Disable `toc` when another package
or custom class owns TOC presentation. Standard `article`, `report`, and `book`
classes are tested.

### Document title (`title`)

`title=true` applies the heading family and `TechnicaInk` to the title, author,
and date rendered by `\maketitle`. The title is bold; author and date use regular
weight. It is included in `style=all`, but not in
`layout=true`. Use `style=all,title=false` to retain the host title-block fonts.
Title styling works independently of `fonts` and `headings`; with fonts disabled,
it uses the host sans family.

The class retains its title, author, and date sizes, spacing, alignment,
and title-page behavior. Standard `article`, `report`, and `book` titles use
this styling. Custom title implementations that do not render `\@title`, or
that explicitly select another font inside the title text, may bypass it.

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

Listings use inset filename headers; terminals use a warmer header with the
heading family. Callout labels sit inside the tinted panel beside its accent
rule. Padding options specify the interior inset, without extra box padding.

| Option | Code default | Callout default |
| --- | --- | --- |
| `arc` | `3pt` | `3pt` |
| `left`, `right` | `8pt`, `8pt` | `10pt`, `12pt` |
| `top`, `bottom` | `8pt`, `8pt` | `8pt`, `8pt` |
| `beforeskip`, `afterskip` | `10pt plus 2pt minus 1pt` | `10pt plus 2pt minus 1pt` |
| `boxrule` | `0.4pt` | Not applicable |
| `languages` | `{cpp,sh}`; empty loads no language definitions | Not applicable |
| `leftrule` | Not applicable | `3pt` |
| `backmix`, `titlemix` | Not applicable | `6`, `6`; percentage of accent mixed into the page color |

### Prose macros (`macroopts`)

| Option | Default / behavior |
| --- | --- |
| `sets` | `prose`; empty loads no macro sets |
| `keypadding` | `1.25pt` |
| `keyrule` | `0.5pt` |
