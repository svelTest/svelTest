# ---------------------------------------------------------
# svelYacc.py
#
# parser for svelTest programs
# ---------------------------------------------------------

# import lexer
from svelLex import SvelLexer

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
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),  
)

def getParser():
    return yacc.yacc()

def p_translation_unit(p):
    '''
    translation_unit : external_declaration
                     | translation_unit external_declaration
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2]

def p_external_declaration(p):
    '''
    external_declaration : function_def
                         | type ID SEMICOLON
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + ";"

def p_function_def(p):
    '''
    function_def : type function_expr brack_stmt
                 | VOID ID function_expr brack_stmt
                 | MAIN LPAREN param_list RPAREN brack_stmt
    '''
    if len(p) == 4:
        p[0] = p[1] + " " + p[2] + " " + p[3]
    elif len(p) == 5:
        p[0] = "void " + p[2] + " " + p[3] + " " + p[4]
    else:
        p[0] = "main(" + p[3] + ") " + p[5]
        print "Got to main"

def p_function_expr(p):
    '''
    function_expr : ID LPAREN param_list RPAREN
    '''
    p[0] = p[1] + "(" + p[3] + ")"
    
def p_type(p):
    '''
    type : svel_type LBRACKET RBRACKET
         | svel_type
    '''
    if len(p) == 4:
        p[0] = p[1] + "[]"
    else:
        p[0] = p[1]

def p_svel_type(p):
    '''
    svel_type : INT 
              | DOUBLE 
              | BOOLEAN 
              | CHAR 
              | STRING 
              | FUNCT 
              | INPUT 
              | OUTPUT 
              | FILE
    '''
    p[0] = p[1] 

def p_param_list(p):
    '''
    param_list : param_list COMMA parameter
               | parameter
    '''
    if len(p) == 4:
        p[0] = p[1] + ", " + p[3]
    else:
        p[0] = p[1]

def p_parameter(p):
    '''
    parameter : type ID
              | empty
    '''
    if len(p) == 3:
        p[0] = p[1] + " " + p[1]
    else:
        p[0] = ""

def p_brack_stmt(p):
    '''
    brack_stmt : LBRACE statements RBRACE
    '''
    p[0] = "{" + p[2] + "}"
    
def p_statements(p):
    '''
    statements : statements stmt
               | stmt
               | brack_stmt
    '''
    if len(p) == 3:
        p[0] = p[1] + " " + p[2]
    else:
        p[0] = p[1]

def p_stmt(p):
    '''
    stmt : expression_stmt
         | ifelse_stmt
         | loop_stmt
         | jump_stmt
    '''
    p[0] = p[1]
    print p[0]

def p_expression_stmt(p):
    '''
    expression_stmt : expression SEMICOLON
    '''
    p[0] = p[1] + ";"
    
def p_expression(p):
    '''
    expression : PRINT assignment_expr
    		   | assignment_expr
               | empty
    '''
    if p[1] == None:
    	p[0] = ""
    else:
    	p[0] = p[1]
    
# TODO: FUNCT is janky
def p_assignment_expr(p):
    '''
    assignment_expr : FUNCT ID ASSIGN LBRACE funct_name COMMA LPAREN reserved_languages_list RPAREN COMMA ID RBRACE
    				| type ID ASSIGN LBRACE assignment_expr RBRACE
    				| type ID ASSIGN assignment_expr
                    | logical_OR_expr
    '''
    if len(p) == 12:
    	p[0] = "funct " + p[2] + " = {" + p[5] + ", (" + p[8] + "), " + p[11] + "}"
    elif len(p) == 11:
    	p[0] = "funct " + p[2] + " = {" + p[5] + ", (), " + p[11] + "}" 
    elif len(p) == 5:
        p[0] = p[1] + " " + p[2] + " " + p[3] + " " + p[4]
    elif len(p) == 7:
        p[0] = p[1] + " " + p[2] + " = {" + p[4] + " }"
    elif len(p) == 3:
        p[0] = "print " + p[2]
    else:
        p[0] = p[1]
def p_funct_name(p):
	'''
	funct_name : __MAIN__ 
			   | ID
	'''
	p[0] = p[1]

def p_logical_OR_expr(p):
    '''
    logical_OR_expr : logical_AND_expr
                    | logical_OR_expr OR logical_AND_expr    
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " || " + p[3]
    
def p_logical_AND_expr(p):
    '''
    logical_AND_expr : equality_expr
                     | logical_AND_expr AND equality_expr
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " && " + p[3]

def p_equality_expr(p):
    '''
    equality_expr : relational_expr
                  | equality_expr EQ relational_expr
                  | equality_expr NEQ relational_expr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "=":
        p[0] = p[1] + " = " + p[3]
    else:
        p[0] = p[1] + " != " + p[3]

def p_relational_expr(p):
    '''
    relational_expr : additive_expr
                    | relational_expr LS_OP additive_expr
                    | relational_expr LE_OP additive_expr
                    | relational_expr GR_OP additive_expr
                    | relational_expr GE_OP additive_expr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "<":
        p[0] = p[1] + " < " + p[3]
    elif p[2] == "<=":
        p[0] = p[1] + " <= " + p[3]
    elif p[2] == ">":
        p[0] = p[1] + " > " + p[3]
    else:
        p[0] = p[1] + " >= " + p[3]
    
def p_additive_expr(p):
    '''
    additive_expr : multiplicative_expr
                  | additive_expr PLUS multiplicative_expr
                  | additive_expr MINUS multiplicative_expr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "+":
        p[0] = p[1] + " + " + p[3]
    else:
        p[0] = p[1] + " - " + p[3]
        
def p_multiplicative_expr(p):
    '''
    multiplicative_expr : prefix_expr
                        | multiplicative_expr TIMES prefix_expr
                        | multiplicative_expr DIVIDE prefix_expr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "*":
        p[0] = p[1] + " * " + p[3]
    else:
        p[0] = p[1] + " / " + p[3]
    
def p_prefix_expr(p):
    '''
    prefix_expr : postfix_expr
                | PLUS PLUS prefix_expr
                | MINUS MINUS prefix_expr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == "+":
        p[0] = "++" + p[3]
    else:
        p[0] = "--" + p[3]
    
def p_postfix_expr(p):
    '''
    postfix_expr : secondary_expr
                 | postfix_expr PLUS PLUS
                 | postfix_expr MINUS MINUS
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "+":
        p[0] = p[1] + "++"
    else:
        p[0] = p[1] + "--"
    
def p_secondary_expr(p):
    '''
    secondary_expr : function_call
                   | LPAREN reserved_languages_list RPAREN
                   | LPAREN expression RPAREN
                   | LBRACE identifier_list RBRACE
                   | primary_expr
    '''
    if p[1] == "(":
        p[0] = "(" + p[2] + ")"
    elif p[1] == "{":
        p[0] = "{" + p[2] + "}" 
    else:
        p[0] = p[1]

def p_primary_expr(p):
    '''
    primary_expr : ID
                 | STRINGLITERAL
                 | constant
    '''
    p[0] = p[1]
     

def p_function_call(p):
    '''
    function_call : ID PERIOD ASSERT LPAREN ID COMMA ID RPAREN
                  | ID PERIOD ID LPAREN identifier_list RPAREN
                  | ID LPAREN identifier_list RPAREN
    '''
    if len(p) == 9:
        p[0] = p[1] + ".assert(" + p[5] + ", " + p[7] + ")"
    elif len(p) == 7:
        p[0] = p[1] + "." + p[3] + "(" + p[5] + ")"
    else:
        p[0] = "(" + p[3] + ")"
    
def p_reserved_languages_list(p):
    '''
    reserved_languages_list : reserved_language_keyword
                            | reserved_languages_list COMMA reserved_language_keyword
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ", " + p[3]

def p_reserved_language_keyword(p):
    '''
    reserved_language_keyword : RES_LANG LBRACKET RBRACKET
    						  | RES_LANG
    '''
    if p[1] == None:
    	p[0] = ""
    else:
    	p[0] = p[1]

def p_identifier_list(p):
    '''
    identifier_list : expression
                    | identifier_list COMMA expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ", " + p[3]

def p_constant(p):
    '''
    constant : NUMBER
             | CHARACTERLITERAL
             | TRUE
             | FALSE
    '''
    p[0] = str(p[1])
    
def p_ifelse_stmt(p):
    '''
    ifelse_stmt : IF LPAREN expression RPAREN stmt
                | IF LPAREN expression RPAREN stmt ELSE stmt
    '''
    if len(p) == 6:
        p[0] = "if(" + p[3] + ")" + p[5]
    else:
        p[0] = "if(" + p[3] + ")" + p[5] + "else" + p[7]

def p_loop_stmt(p):
    '''
    loop_stmt : WHILE LPAREN expression RPAREN stmt
              | FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN stmt
    '''
    if len(p) == 5:
        p[0] = "while(" + p[3] + ")" + p[5]
    else:
        p[0] = "for(" + p[3] + "; " + p[5] + "; " + p[7] + ")" + p[9]

def p_jump_stmt(p):
    '''
    jump_stmt : BREAK SEMICOLON
              | CONTINUE SEMICOLON
              | RETURN expression SEMICOLON
    '''
    if p[1] == "break":
        p[0] = "break;"
    elif p[1] == "continue":
        p[0] = "continue;"
    else:
        p[0] = "return " + p[2] + ";" 
    
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