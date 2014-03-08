%{
#include <stdio.h>
#define YYSTYPE char
%}

%token FILE_TYPE
%token STRINGLITERAL
%token VARIABLE
%token NUMBER
%token NOTVALID

%%

expr 	: FILE_TYPE VARIABLE '=' STRINGLITERAL ';' { printf("expr"); }
	;
%%

#include "lex.yy.c"
