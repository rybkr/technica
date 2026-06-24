# Technica

Technica is a small LaTeX style system for technical writing: tutorials, course notes, reference material, engineering reports, and code-heavy articles.

The public entry point is:

```latex
\usepackage{technica}
```

## Public API

Inline technical prose:

```latex
\term{translation unit}
\filepath{src/main.cpp}
\command{clang++}
\api{std::vector}
\key{Esc}
```

Inline code:

```latex
\inlinecode{generic code}
\inlinecxx{std::vector<int>}
\inlinesh{clang++ main.cpp}
```

Block environments:

```latex
\begin{cxx}{main.cpp}
int main() {
    return 0;
}
\end{cxx}

\begin{terminal}
$ clang++ main.cpp
$ ./a.out
\end{terminal}

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

## Development Usage

From a consuming repository, point `TEXINPUTS` at this checkout:

```sh
TEXINPUTS=/path/to/technica//: xelatex chapters/example/example.tex
```

Then documents can use the clean package name:

```latex
\usepackage{technica}
```

To compile the included example from this repository:

```sh
cd examples
TEXINPUTS=..//: xelatex article.tex
```

To compile the smoke test:

```sh
cd test
TEXINPUTS=..//: xelatex smoke.tex
```

XeLaTeX or LuaLaTeX is recommended. pdfLaTeX has a fallback path, but system
font selection is better with modern engines.
