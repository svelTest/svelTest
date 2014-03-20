analyzeSvelFile: lex.yy.c
	gcc lex.yy.c -ll -o analyzeSvelFile

lex.yy.c: svelLex.l
	lex svelLex.l

.PHONY: clean
clean: 
	rm analyzeSvelFile lex.yy.c
