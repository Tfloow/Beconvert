TEX = pandoc
src = template.tex details.yml
FLAGS = --pdf-engine=xelatex

output.pdf : $(src)
	$(TEX) $(filter-out $<,$^ ) -o $@ --template=$< $(FLAGS)

%: template.tex ../../uploads/%/details.yml
	$(TEX) $(filter-out $<,$^ ) -o ../../uploads/$@/output.tex --template=$< $(FLAGS)
	$(TEX) $(filter-out $<,$^ ) -o ../../uploads/$@/output.pdf --template=$< $(FLAGS)

.PHONY: clean
clean :
	rm output.pdf
