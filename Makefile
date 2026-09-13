.PHONY: install-hooks bundle

TEXMFLOCAL ?= $(shell kpsewhich -var-value TEXMFLOCAL 2>/dev/null || printf '%s\n' /usr/local/texlive/texmf-local)
INSTALL_DIR := $(TEXMFLOCAL)/tex/latex/technica

SRC := technica.sty \
       technica-colors.sty \
       technica-fonts.sty \
       technica-layout.sty \
       technica-code.sty \
       technica-boxes.sty \
       technica-macros.sty \
       macros/prose.def \
       languages/cxx.def \
       languages/sh.def \
       themes/technica-colors-light.def \
       themes/technica-colors-dark.def

install-hooks:
	git config core.hooksPath .githooks

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
