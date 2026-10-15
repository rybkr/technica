#!/usr/bin/env python3
"""Compile regression fixtures against this checkout, never an installed copy."""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "tests"


def compile_tex(engine, name, source, passes=1, expected_error=None):
    destination = BUILD / engine / name
    destination.mkdir(parents=True, exist_ok=True)
    tex = destination / f"{name}.tex"
    tex.write_text(source)
    # tcolorbox rereads generated .listing files; prefer this case's working
    # directory over artifacts from another engine below the recursive root.
    env = dict(os.environ, TEXINPUTS=f".:{ROOT}//:" + os.environ.get("TEXINPUTS", ""))
    for _ in range(passes):
        result = subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", str(tex)],
            cwd=destination, env=env, capture_output=True, text=True,
        )
        (destination / "compile.txt").write_text(result.stdout + result.stderr)
        if expected_error is not None:
            # TeX wraps diagnostics even in the middle of words.
            if result.returncode and "".join(expected_error.split()) in "".join(result.stdout.split()):
                return None
            raise RuntimeError(f"{engine}/{name}: expected error {expected_error!r}\n{result.stdout[-2500:]}")
        if result.returncode:
            raise RuntimeError(f"{engine}/{name}: compilation failed\n{result.stdout[-2500:]}")
    return destination / f"{name}.pdf"


def pdf_text(pdf):
    return subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], text=True)


def require_text(text, *literals):
    for literal in literals:
        if literal not in text:
            raise RuntimeError(f"Missing literal {literal!r} in PDF text: {text!r}")


def document(options, body="Module switches work.", document_class="article"):
    return (
        rf"\documentclass{{{document_class}}}" "\n"
        rf"\usepackage[{options}]{{technica}}" "\n"
        rf"\begin{{document}}{body}\end{{document}}" "\n"
    )


def cases():
    for name in ("defaults", "inline", "layout", "blocks", "title", "callouts",
                 "prose-literals", "definition-loading", "definition-lists",
                 "preloaded-boxes", "late-fonts", "colors", "cpp-keywords",
                 "listing-defaults", "number-gutter", "number-gutter-color"):
        yield name, (ROOT / "tests" / f"{name}.tex").read_text(), 2 if name == "blocks" else 1
    components = (ROOT / "examples/components.tex").read_text()
    for theme in ("light", "dark"):
        yield f"components-{theme}", rf"\PassOptionsToPackage{{theme={theme}}}{{technica}}" + "\n" + components, 2
    config_template = (ROOT / "tests/config.tex").read_text()
    for reverse in (False, True):
        options = ["config={tests/course.cfg}", "theme=light", "codeopts={arc=0pt}"]
        if reverse:
            options.reverse()
        yield f"config-{reverse}", config_template.replace("CONFIG_OPTIONS", ",".join(options)), 1
    for languages in ("sh", ""):
        source = document(
            "config={tests/course.cfg},codeopts={languages={" + languages + "}},macroopts={sets={}}",
            r"\makeatletter\@ifundefined{inlinecpp}{}{\errmessage{Language list was merged}}"
            r"\@ifundefined{term}{}{\errmessage{Macro list was merged}}\makeatother Lists replaced.",
        )
        yield f"config-lists-{languages or 'empty'}", source, 1
    yield "config-disabled", document(
        "config={tests/course.cfg},code=false",
        r"\makeatletter\@ifpackageloaded{technica-code}{\errmessage{Code was enabled}}{}"
        r"\makeatother Disabled module stays disabled.",
    ), 1
    yield "config-preset", document(
        "config={tests/course.cfg},style=all,fonts=false,hyperlinks=false",
        r"\makeatletter\iftechnica@main@headingsenabled\errmessage{Preset overrode explicit switch}\fi"
        r"\iftechnica@main@pagecolorsenabled\else\errmessage{Preset not applied}\fi"
        r"\makeatother Preset resolved after merging.",
    ), 1
    style_features = ("fonts", "title", "headings", "paragraphs", "lists", "captions", "pagecolors", "hyperlinks")
    template = (ROOT / "tests/global-styles.tex").read_text()
    style_cases = [(f"style-only-{feature}", feature, {feature}) for feature in style_features]
    style_cases.append(("style-all", "style=all", set(style_features)))
    style_cases.append(("style-layout", "layout=true", {"headings", "paragraphs", "lists", "captions"}))
    for feature in style_features:
        for reverse in (False, True):
            options = ["style=all", f"{feature}=false"]
            if reverse:
                options.reverse()
            style_cases.append((f"style-override-{feature}-{reverse}", ",".join(options), set(style_features) - {feature}))
    for name, options, enabled in style_cases:
        assertions = []
        for feature, saved, current in (
            ("headings", "savedsection", "section"),
            ("captions", "savedcaption", "@makecaption"),
            ("pagecolors", "savedpage", "recordedpage"),
            ("pagecolors", "savedink", "current@color"),
            ("hyperlinks", "savedlink", "@linkcolor"),
        ):
            error = rf"\errmessage{{Unexpected {feature} styling}}"
            branches = error + r"\else" if feature in enabled else r"\else" + error
            assertions.append(rf"\ifx\{saved}\{current}{branches}\fi")
        assertions.append(
            r"\begin{itemize}\item Test."
            + (r"\ifdim\itemsep=2pt\else\errmessage{List spacing missing}\fi"
               if "lists" in enabled else
               r"\ifdim\itemsep=4pt\else\errmessage{List spacing changed}\fi")
            + r"\end{itemize}"
        )
        indent, skip = (0, 6) if "paragraphs" in enabled else (19, 3)
        assertions.extend([
            rf"\ifdim\parindent={indent}pt\else\errmessage{{Wrong paragraph indent}}\fi",
            rf"\ifdim\parskip={skip}pt\else\errmessage{{Wrong paragraph spacing}}\fi",
            r"\@ifpackageloaded{technica-fonts}" + (
                r"{}{\errmessage{Fonts not enabled}}" if "fonts" in enabled
                else r"{\errmessage{Fonts unexpectedly enabled}}{}"
            ),
        ])
        title_assertion = (
            r"\begingroup\technicaheadingfont"
            if "title" in enabled else r"\begingroup\normalfont"
        ) + (
            r"\xdef\expectedfamily{\f@family}\xdef\expectedseries{\f@series}\endgroup"
            r"\ifx\f@family\expectedfamily\else\errmessage{Wrong title family}\fi"
            r"\ifx\f@series\expectedseries\else\errmessage{Wrong title weight}\fi"
        )
        metadata_assertion = (
            r"\begingroup\normalfont\technicaheadingfamily"
            if "title" in enabled else r"\begingroup\normalfont"
        ) + (
            r"\xdef\expectedfamily{\f@family}\xdef\expectedseries{\f@series}\endgroup"
            r"\ifx\f@family\expectedfamily\else\errmessage{Wrong author/date family}\fi"
            r"\ifx\f@series\expectedseries\else\errmessage{Wrong author/date weight}\fi"
        )
        yield name, template.replace("GLOBAL_OPTIONS", options).replace("GLOBAL_ASSERTIONS", "\n".join(assertions)).replace("TITLE_ASSERTIONS", title_assertion).replace("METADATA_ASSERTIONS", metadata_assertion), 1
    title_template = (ROOT / "tests/title-styling.tex").read_text()
    for cls, cls_options in (("article", ""), ("article", "titlepage"),
                             ("article", "twocolumn"), ("report", ""), ("book", "")):
        yield f"title-styling-{cls}-{cls_options or 'default'}", title_template.replace("DOCUMENT_CLASS", cls).replace("CLASS_OPTIONS", cls_options), 1
    features = ("fonts", "layout", "code", "boxes", "macros")
    bodies = {
        "fonts": "Font module only.",
        "layout": r"\section{Layout module only}Independent headings.",
        "code": "\\begin{cpp}{Module only}\nint value = 1;\n\\end{cpp}\n",
        "boxes": r"\begin{note}Callout module only.\end{note}",
        "macros": r"\term{Term} \filepath{src/main.cpp} \key{Esc}",
    }
    for active in (None,) + features:
        options = ",".join(f"{feature}={'true' if feature == active else 'false'}" for feature in features)
        yield f"only-{active or 'none'}", document(options, bodies.get(active, "All modules disabled.")), 1
    yield "no-fonts", document("fonts=false,layout=true", r"\section{Fallback headings}\begin{note}Fallback callout.\end{note}"), 1
    for cls in ("report", "book"):
        yield cls, document("fonts=true,layout=true", r"\title{Class title}\author{Technica}\maketitle\chapter{Class chapter}\section{Section}Body.", cls), 1
    yield "long-callout", document("pagecolors=true,theme=dark",
        r"\begin{explanation}" + "\n\n".join(
            f"Paragraph {i}: Keep the timing calculation separate from the operation that waits. "
            "A pure calculation is easier to inspect and test with exact expected values."
            for i in range(40)
        ) + r"\end{explanation}"), 1
    yield "long-code", document("", "\\begin{cpp}{Long listing}\n" + "\n".join(
        f"int item{i} = {i};" for i in range(100)
    ) + "\n\\end{cpp}\n"), 1


def check_case(name, pdf):
    text = pdf_text(pdf)
    if name == "number-gutter-color":
        xml = ET.fromstring(subprocess.check_output(
            ["pdftohtml", "-xml", "-stdout", str(pdf)], text=True,
        ))
        colors = {font.get("id"): font.get("color") for font in xml.iter("fontspec")}
        for phrase in ("Body ink after listing.", "Body ink on next page."):
            matches = [node for node in xml.iter("text") if phrase in "".join(node.itertext())]
            if len(matches) != 1:
                raise RuntimeError(f"Expected one rendered paragraph: {phrase}")
            color = colors[matches[0].get("font")]
            actual = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
            # Drivers differ by one quantization step when converting to RGB.
            if any(abs(a - b) > 1 for a, b in zip(actual, (232, 236, 241))):
                raise RuntimeError(f"Body ink changed after gutter measurement: {color}")
    elif name.startswith("components-"):
        require_text(text, "retry.cpp", "Build and inspect", "All checks passed.")
    elif name in ("config-False", "config-True"):
        require_text(text, "Spaces are preserved", "Second hook", "Design rule", "file_name")
    elif name == "inline":
        require_text(text, "left || right", "left | right", "cat input | sort",
                     "100% literal #1 $HOME file_name & value",
                     "if (a || b) { return a | b; }", r'''printf '%s\n' "$HOME" | sort''',
                     r"C:\tmp\file_name", "unmatched } and { braces")
    elif name == "prose-literals":
        require_text(text, "clang++ --version", r"C:\Users\ryan\file.txt",
                     "my--file.txt", "operator--",
                     "100% literal #1 $HOME file_name & value",
                     r'''printf '%s\n' "$HOME" | sort''', "if (ready) { run(); }")
    elif name == "definition-loading":
        require_text(text, "first", "second", "Second term", "$ make")
    elif name == "blocks":
        # Check numbering, source slicing, factory options, and resolved labels.
        for number, code in ((20, "int first = 20;"), (21, "int second = 21;"),
                             (30, "custom = works"), (35, "$ cat input | sort"),
                             (40, "int imported = 40;"), (41, "int selected = 41;")):
            if not re.search(rf"(?m)^\s*{number}\s+{re.escape(code)}", text):
                raise RuntimeError(f"Missing numbered line {number}: {code!r}")
        if not re.search(r"(?m)^\s*int plain = 0;", text):
            raise RuntimeError("numbers=none did not suppress line numbers")
        require_text(" ".join(text.split()), "First block: 1. Source block: 6.", "legacy = works", "Build session")
        if "EXCLUDED" in text:
            raise RuntimeError("Source inclusion ignored firstline/lastline")
    elif name.startswith("title-styling-"):
        require_text(text, "Styled title", "Author retained", "Date retained",
                     "Body retained.", "Acknowledgment retained.", "Author note retained.",
                     "Second author")
    elif name == "title":
        require_text(text, "Custom title retained.")
    elif name == "long-callout":
        require_text(text, "Paragraph 0:", "Paragraph 39:")
        if text.count("\f") < 2:
            raise RuntimeError("Long callout did not span pages")
    elif name == "long-code":
        require_text(text, "int item0 = 0;", "int item99 = 99;")
        if text.count("\f") < 2:
            raise RuntimeError("Long listing did not span pages")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("engines", nargs="*", default=["pdflatex", "xelatex", "lualatex"])
    args = parser.parse_args()
    engines = args.engines
    for tool in engines + ["pdftotext", "pdftohtml"]:
        if not shutil.which(tool):
            raise RuntimeError(f"Required tool not found: {tool}")
    failures = []
    for engine in engines:
        for name, source, passes in cases():
            try:
                pdf = compile_tex(engine, name, source, passes)
                check_case(name, pdf)
                log = pdf.with_suffix(".log").read_text()
                if "Overfull \\hbox" in log or "Overfull \\vbox" in log:
                    raise RuntimeError(f"{engine}/{name}: overflowing content; see {pdf.with_suffix('.log')}")
                if "undefined references" in log:
                    raise RuntimeError(f"{engine}/{name}: unresolved references")
                print(f"PASS {engine}/{name}", flush=True)
            except RuntimeError as error:
                failures.append(str(error))
                print(f"FAIL {engine}/{name}", flush=True)
        for name, options, body, error in (
            ("missing", "config={tests/nonexistent.cfg}", "", "Configuration file"),
            ("unknown", "config={tests/config-unknown.cfg}", "", "undefined"),
            ("nested", "config={tests/config-nested.cfg}", "", "Nested config selection"),
            ("module-unknown", "codeopts={unknownsetting=1}", "", "unknownsetting"),
            ("late", "", r"\technicasetup{theme=dark}", "Configuration is already closed"),
            ("late-hook", "", r"\technicaaftersetup{}", "Configuration is already closed"),
        ):
            try:
                compile_tex(engine, f"config-error-{name}", document(options, body), expected_error=error)
                print(f"PASS {engine}/config-error-{name}", flush=True)
            except RuntimeError as error:
                failures.append(str(error))
                print(f"FAIL {engine}/config-error-{name}", flush=True)
    if failures:
        raise RuntimeError("\n\n".join(failures))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        sys.exit(str(error))
