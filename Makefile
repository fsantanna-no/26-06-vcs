TEX = pdflatex -interaction=nonstopmode -halt-on-error

all: main.pdf

main.pdf: main.tex main.bib
	$(TEX) main
	bibtex main
	$(TEX) main
	$(TEX) main

clean:
	rm -f main.aux main.log main.bbl main.blg main.out main.toc

.PHONY: all clean cleanall
