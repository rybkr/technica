.PHONY: install-hooks bundle test demo

PYTHON ?= python3
ENGINES ?= pdflatex xelatex lualatex
ENGINE ?= xelatex

TEXMFLOCAL ?= $(shell kpsewhich -var-value TEXMFLOCAL 2>/dev/null || printf '%s\n' /usr/local/texlive/texmf-local)
INSTALL_DIR := $(TEXMFLOCAL)/tex/latex/technica

SRC := technica.sty \
       technica-colors.sty \
       technica-definitions.sty \
       technica-fonts.sty \
       technica-layout.sty \
       technica-code.sty \
       technica-boxes.sty \
       technica-macros.sty \
       macros/prose.def \
       languages/cpp.def \
       languages/sh.def \
       themes/technica-colors-light.def \
       themes/technica-colors-dark.def

install-hooks:
	git config core.hooksPath .githooks

test:
	$(PYTHON) scripts/test.py $(ENGINES)

demo:
	@mkdir -p build/demo output/pdf
	@set -e; cd build/demo; \
	for pass in 1 2; do \
		TEXINPUTS=".:$(CURDIR)//:" $(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error "$(CURDIR)/examples/demo.tex"; \
	done
	@install -m 0644 build/demo/demo.pdf output/pdf/technica-demo.pdf
	@printf '%s\n' "Demo written to output/pdf/technica-demo.pdf"

bundle:
	@set -e; \
	for path in $(SRC); do \
		install -d "$(INSTALL_DIR)/$$(dirname "$$path")"; \
		install -m 0644 "$$path" "$(INSTALL_DIR)/$$path"; \
	done; \
	if command -v texhash >/dev/null 2>&1; then \
		texhash "$(TEXMFLOCAL)"; \
	fi; \
	printf '%s\n' "Installed technica package to $(INSTALL_DIR)"
