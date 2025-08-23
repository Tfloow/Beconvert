TEX = pandoc
src = letter.md
template= letter.latex
FLAGS = --template="$(template)"

# Overwritten when calling make XXXXX-.... OUTPUT_FILE_TYPE=...
OUTPUT_FILE_TYPE=.pdf

output.pdf : $(src)
	$(TEX) $< -o $@ $(FLAGS)

%: header.md ../../uploads/%/input.md
	$(TEX) $^ -o ../../uploads/$@/output$(OUTPUT_FILE_TYPE) $(FLAGS)

.PHONY: clean
clean :
	rm output.pdf
