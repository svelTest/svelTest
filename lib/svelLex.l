%{
	#include <stdio.h>
%}

import		"import"
test		"test"
test_func	"test()"
int		"int"
function	"function"
param		"param"
output		"output"
testcase	"testcase"
SYSOUT		"SYSOUT"
MAIN		"MAIN"
TESTCASE	"TESTCASE"
FUNCTION	"FUNCTION"
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
comment		\/\*[^\/\*]*\*\/
delim		[ \t\n]
ws		{delim}+

%%

{import}	{ printf("IMPORT"); }
{test}		{ printf("TEST"); }
{test_func}	{ printf("TESTfunction"); }
{int}		{ printf("INT"); }
{function}	{ printf("FUNCTION"); }
{param}		{ printf("PARAM"); }
{output}	{ printf("OUTPUT"); }
{testcase}	{ printf("TESTCASE"); }
{SYSOUT}	{ printf("SYSOUTkeyword"); }
{MAIN}		{ printf("MAINkeyword"); }
{TESTCASE}	{ printf("TESTCASEkeyword"); }
{FUNCTION}	{ printf("FUNCTIONkeyword"); }
{main}		{ printf("MAIN()"); }
{boolean}	{ printf("BOOLEAN"); }
{if}		{ printf("IF"); }
{else}		{ printf("ELSE"); }
{while}		{ printf("WHILE"); }
{print}		{ printf("PRINT"); }
{stringLiteral}	{ printf("%s", yytext); }
{variable}	{ printf("%s", yytext); }

{number}	{ printf("%s", yytext); }
{notvalid}	{ printf("NOT VALID"); }
{comment}	{ printf("COMMENT"); }
{delim}		{ printf("%s", yytext); /* will eventually want to skip blanks */ }
\n|.		{ printf("%s", yytext); }

%%

int main() {
	yylex();
	return 0;
}

