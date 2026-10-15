#!/usr/bin/env python3
"""Compile regression fixtures against this checkout, never an installed copy."""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "tests"


def compile_tex(engine, name, source, passes=1):
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
    for name in ("inline", "layout", "blocks", "title", "callouts",
                 "prose-literals", "definition-loading", "definition-lists",
                 "preloaded-boxes", "late-fonts", "colors", "cpp-keywords",
                 "listing-defaults", "number-gutter"):
        yield name, (ROOT / "tests" / f"{name}.tex").read_text(), 2 if name == "blocks" else 1
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
    yield "no-fonts", document("fonts=false", r"\section{Fallback headings}\begin{note}Fallback callout.\end{note}"), 1
    for cls in ("report", "book"):
        yield cls, document("", r"\title{Class title}\author{Technica}\maketitle\chapter{Class chapter}\section{Section}Body.", cls), 1
    yield "long-code", document("", "\\begin{cpp}{Long listing}\n" + "\n".join(
        f"int item{i} = {i};" for i in range(100)
    ) + "\n\\end{cpp}\n"), 1


def check_case(name, pdf):
    text = pdf_text(pdf)
    if name == "inline":
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
    elif name == "title":
        require_text(text, "Custom title retained.")
    elif name == "long-code":
        require_text(text, "int item0 = 0;", "int item99 = 99;")
        if text.count("\f") < 2:
            raise RuntimeError("Long listing did not span pages")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("engines", nargs="*", default=["pdflatex", "xelatex", "lualatex"])
    args = parser.parse_args()
    engines = args.engines
    for tool in engines + ["pdftotext"]:
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
    if failures:
        raise RuntimeError("\n\n".join(failures))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        sys.exit(str(error))
