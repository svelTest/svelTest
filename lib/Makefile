main: lex.yy.c
	gcc lex.yy.c -ly -ll -o main

lex.yy.c: svelLex.l
	lex svelLex.l

.PHONY: clean
clean:
	rm -f *.o *.c *~ main a.out core
