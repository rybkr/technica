---
name: Technica
description: Create and edit LaTeX documents using the Technica style package. Use when the user requests Technica styling or the document already loads Technica.
---

# Technica

For a new document requesting Technica's built-in styling, start with:

```latex
\documentclass{article}
\usepackage[style=all]{technica}
\usepackage{hyperref}
\title{Document title}
\author{Author}
\date{\today}
\begin{document}
\maketitle
\section{Introduction}
Document text.
\end{document}
```

Preserve an existing document's class, configuration, and explicit font choices.
Plain `\usepackage{technica}` enables components only; `style=all` also enables
fonts, title, headings, paragraphs, lists, captions, page colors, and link styling.
Individual switches override the preset. `title=false` preserves host title-block
fonts; `layout=true` does not enable title styling. Technica leaves page geometry
and title placement to the class. `article` is supported; basic `report` and
`book` are tested, with chapter styling left to the class.

## Authoring

- Use `\term`, `\filepath`, `\command`, `\api`, and `\key` for semantic prose.
- Use `\inlinecode`, `\inlinecpp`, or `\inlinesh` for short code; use
  `codeblock` and `cpp` environments with a required title, or `terminal`
  without one, for blocks. C++ blocks have line numbers by default.
- Choose `note`, `explanation`, `advice`, or `warning` by meaning.
- Literal prose commands (`\filepath`, `\command`, `\api`) and inline code
  must stay on one source line, directly in paragraph text. Do not nest them
  inside headings, captions, or other command arguments. Use delimiter syntax
  for literal closing braces, e.g. `\inlinecpp!if (ready) { run(); }!`.
- For a dark document, use `theme=dark,pagecolors=true` (or `style=all,theme=dark`).
  The theme alone does not change the page background.

Read the relevant sections of the [reference](../../docs/reference.md) for
module options, reusable configurations, source-file listings, or extension
factories. Prefer these APIs over patching package internals. For configuration
files, document options override file settings; module option lists merge by
key, while list values are replaced.

## Build and check

Prefer XeLaTeX or LuaLaTeX for system fonts; pdfLaTeX is supported. Resolve the
actual checkout path instead of assuming Technica is installed:

```sh
TEXINPUTS=.:/path/to/technica//: xelatex document.tex
```

Run from the document's working directory; keep the leading `.` and trailing
`:` in `TEXINPUTS`. Compile twice when resolving references. Check the log for
errors, unresolved references, and overfull boxes, and inspect the PDF when
changing layout. No shell escape or external syntax highlighter is needed.

See the [README](../../README.md) for setup and the
[demo](../../examples/demo.tex) for a complete example. If the task is to change
Technica itself, follow [CONTRIBUTING.md](../../CONTRIBUTING.md) for tests and
package-date conventions. These links are relative to this skill in the checkout;
if the skill is copied elsewhere, locate the checkout containing `technica.sty`.
