TEX = pdflatex -interaction=nonstopmode -halt-on-error

DIAS = $(wildcard imgs/*.dia)
IMGS = $(DIAS:.dia=.pdf)

all: main.pdf

imgs: $(IMGS)

# dia -t pdf paginates on A4, so go through svg + inkscape crop
imgs/%.pdf: imgs/%.dia
	dia -e $(<:.dia=.svg) -t svg $< >/dev/null 2>&1
	inkscape $(<:.dia=.svg) --export-type=pdf --export-area-drawing --export-filename=$@
	rm -f $(<:.dia=.svg)

main.pdf: main.tex main.bib $(IMGS)
	$(TEX) main
	bibtex main
	$(TEX) main
	$(TEX) main

clean:
	rm -f main.aux main.log main.bbl main.blg main.out main.toc

.PHONY: all imgs clean cleanall
