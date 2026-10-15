# Contributing to Technica

See the [README](README.md#installation) for TeX dependencies and installation,
and the [reference](docs/reference.md) for APIs and configuration behavior.
Run the commands below from the repository root.

## Source layout

- `technica.sty` selects modules and resolves configuration and package options.
- `technica-*.sty` implement fonts, layout, colors, code, callouts, prose macros,
  and shared definition loading.
- `languages/*.def`, `macros/*.def`, and `themes/*.def` hold language definitions,
  macro sets, and themes.
- `tests/` contains regression documents and fixtures; `scripts/test.py` selects
  cases, generates option combinations, and checks their output.
- `examples/` contains the demo document and a reusable configuration.

When changing behavior, update the relevant reference documentation and add or
adjust a regression case. New standalone test documents must be registered in
`scripts/test.py` to run with the suite. If adding package or definition files,
update `SRC` in the `Makefile` so `make bundle` installs them.

## Demo

Build the three-page sample in `examples/demo.tex`:

```sh
make demo                         # XeLaTeX
make demo ENGINE=pdflatex         # fallback fonts
```

The PDF is written to `output/pdf/technica-demo.pdf`. It demonstrates semantic
prose, C++ and generic code blocks, terminal sessions, callouts, and references.
Change `theme=light` to `theme=dark` in the source to preview the dark theme.

## Checks

```sh
make test                         # pdfLaTeX, XeLaTeX, and LuaLaTeX
make test ENGINES=pdflatex        # one engine
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
