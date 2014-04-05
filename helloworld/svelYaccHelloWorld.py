# ---------------------------------------------------------
# svelYacc.py
#
# parser for svelTest programs
# ---------------------------------------------------------

# import lexer
from svelLexHelloWorld import SvelLexer
from node import Node

# be able to go into the ply directory to get to the 
# ply modules
import os, sys
lib_path = os.path.join('ply-3.4')
sys.path.append(lib_path)

# import ply (imports from ply-3.4/ply)
import ply.yacc as yacc

# get tokens
tokens = SvelLexer.tokens
# set precedence
precedence = (
)

def getParser(**kwargs):
    return yacc.yacc(**kwargs)

def p_main_stmt(p):
    '''
    main_stmt : MAIN LPAREN RPAREN LBRACE print_stmt RBRACE
    '''
    #p[0] = "main() {\n" + p[5] + "\n}"
    p[0] = Node("main_stmt", [p[5]], "main");

def p_print_stmt(p):
    '''
    print_stmt : PRINT STRINGLITERAL SEMICOLON
    '''	
    #p[0] = "print " + p[2] + ";"
    p[0] = Node("print_stmt", [Node("STRINGLITERAL", [], p[2])], "print");
    
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    # we should throw compiler error in this case 
    if p == None: 
        print "Syntax error at last token." 
    else: 
        print "Syntax error around line number \n %d : %s " % (p.lineno, p.value) 


if __name__ == '__main__':
    # get and build lexer
    svel = SvelLexer()
    svel.build()

    parser = getParser()

    # loop to get user input
    while True:
        # print prompt and gather input
        try:
            line = raw_input("Enter a string to parse\n")

        # if Ctrl-D, exit
        except EOFError:
            break

        # otherwise, tokenize the string
        print parser.parse(line, lexer=svel.get_lexer())
