.PHONY: poster slides abstract all clean

all: abstract poster slides

abstract:
	cd abstract && quarto render abstract.qmd

poster:
	cd poster && quarto render index.qmd

slides:
	cd slides && quarto render index.qmd

clean:
	find . -name "_output" -o -name ".quarto" | xargs rm -rf
