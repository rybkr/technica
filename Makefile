.PHONY: install-hooks

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
