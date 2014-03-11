%{
	#include <stdio.h>
%}

file		"File"
test		"Test"
main		"main()"
boolean		"boolean"
if		"if"
else		"else"
while		"while"
print		"print"
stringLiteral	\"[^\"]*\"
variable	[a-zA-z_][a-zA-z0-9_]*
number		[0-9]+
notvalid	[0-9]+[a-zA-z0-9_]*
delim		[ \t\n]
ws		{delim}+

%%

{file}		{ printf("FILE"); }
{test}		{ printf("TEST"); }
{main}		{ printf("MAIN"); }
{boolean}	{ printf("BOOLEAN"); }
{if}		{ printf("IF"); }
{else}		{ printf("ELSE"); }
{while}		{ printf("WHILE"); }
{print}		{ printf("PRINT"); }
{stringLiteral}	{ printf("%s", yytext); }
{variable}	{ printf("%s", yytext); }

{number}	{ printf("%s", yytext); }
{notvalid}	{ printf("NOT VALID"); }
{delim}		{ /* skip blanks */ }
\n|.		{ printf(" "); }

%%

int main() {
	yylex();
	return 0;
}

