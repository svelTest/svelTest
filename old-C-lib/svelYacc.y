%{
#include <stdio.h>
%}

%token FILE
%token TEST
%token MAIN
%token BOOLEAN
%token IF
%token ELSE
%token WHILE
%token PRINT
%token STRINGLITERAL
%token VARIABLE
%token NUMBER
%token NOTVALID
%token WS

%%

lines   : lines expr '\n'       {if ($2){
                                    printf("Result: true\n");
                                 } else {
                                    printf("Result: false\n");
                                 }
                                }
        | lines '\n'            
        | /*empty*/
        | error '\n'            {yyerror("reenter previous line:"); yyerrok;}
        ;

expr    : expr NAND term        {$$ = !($1 && $3); }
        | term
        ;

term    : '(' expr ')'          {$$ = $2;}
        | TRUE                  {$$ = 1;}
        | FALSE                 {$$ = 0;}
        ;
%%

#include "lex.yy.c"

int yyerror(char const *message) {
        fputs(message, stderr);
        fputc('\n', stderr);
        return 0;
}
