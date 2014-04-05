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
              | MAIN LPAREN RPAREN LBRACE file_stmt if_else_loop RBRACE
    '''
    #p[0] = "main() {\n" + p[5] + "\n}"
    if len(p) == 7:
        p[0] = Node("main_stmt", [p[5]], "main");
    else:
        p[0] = Node("main_stmt", [p[5], p[6]], "main")

def p_file_stmt(p):
    '''
    file_stmt : FILE ID ASSIGN STRINGLITERAL SEMICOLON
    '''
    p[0] = Node("file_stmt", [Node("ID", [], p[2]), Node("STRINGLITERAL", [], p[4])], "file")

def p_if_else_loop(p):
    '''
    if_else_loop : IF LPAREN ID PERIOD ASSERT RPAREN brack_stmt ELSE brack_stmt
    '''
    p[0] = Node("if_else_loop", [Node("ID", [], p[3]), p[7], p[9]], "if-else")

def p_brack_stmt(p):
    '''
    brack_stmt : LBRACE print_stmt RBRACE
    '''
    p[0] = Node("brack_stmt", [p[2]], "bracketed-statement")

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
