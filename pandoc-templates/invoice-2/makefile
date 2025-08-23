TEX = pandoc
src = letter.md
template= letter
FLAGS = --template="$(template)"

output.pdf : $(src)
	$(TEX) $< -o $@ $(FLAGS)

%: header.md ../../uploads/%/input.md
	$(TEX) $^ -o ../../uploads/$@/output.tex $(FLAGS)
	$(TEX) $^ -o ../../uploads/$@/output.pdf $(FLAGS)

.PHONY: clean
clean :
	rm output.pdf
