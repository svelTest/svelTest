%{
	#include <stdio.h>
%}

file		"File"
stringLiteral	\"[^\"]*\"
variable	[a-zA-z_][a-zA-z0-9_]*
number		[0-9]+
notvalid	[0-9]+[a-zA-z0-9_]*
delim		[ \t\n]
ws		{delim}+

%%

{file}		{ return FILE_TYPE; }
{stringLiteral}	{ return STRINGLITERAL; }
{variable}	{ return VARIABLE; }

{number}	{ return NUMBER; }
{notvalid}	{ return NOTVALID; }
{delim}		{ /* skip blanks */ }
\n|.		{ sscanf(yytext, "%s", &yylval); }

%%
