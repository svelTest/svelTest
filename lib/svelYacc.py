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

# import node class
from node import Node

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
        p[0] = Node('translation_unit', [p[1]])
    else:
        p[0] = Node('translation_unit', [p[1], p[2]])

def p_external_declaration(p):
    '''
    external_declaration : function_def
                         | type ID SEMICOLON
    '''
    if len(p) == 2:
        p[0] = Node('external_declaration', [p[1]])
    else:
        p[0] = Node('translation_unit', [p[1], p[2]])

def p_function_def(p):
    '''
    function_def : VOID ID LPAREN param_list RPAREN brack_stmt
                | type ID LPAREN param_list RPAREN brack_stmt
                | MAIN LPAREN param_list RPAREN brack_stmt
    '''
    if p[1] == "void":
        p[0] = Node('function_def', [Node('VOID', [], p[1]), p[4], p[6]], p[2])
    elif len(p) == 7:
        p[0] = Node('function_def', [p[1], p[4], p[6]], p[2])
    else:
        p[0] = Node('function_def', [p[3], p[5]], "main")

def p_type(p):
    '''
    type : INT 
          | DOUBLE 
          | BOOLEAN 
          | CHAR 
          | STRING 
          | FUNCT 
          | INPUT 
          | OUTPUT 
          | FILE
          | type LBRACKET RBRACKET
    '''
    if len(p) == 2:
        p[0] = Node('type', [], p[1])
    else:
        p[0] = Node('type', [], p[1].leaf + p[2] + p[3])

def p_reslang_type(p):
    '''
    reslang_type : RES_LANG
                | RES_LANG LBRACKET RBRACKET
    '''
    if len(p) == 2:
        p[0] = Node('reslang_type', [], p[1])
    else:
        p[0] = Node('reslang_type', [], p[1].leaf + p[2] + p[3])

def p_param_list(p):
    '''
    param_list : param_list COMMA parameter
               | parameter
    '''
    if len(p) == 4:
        p[0] = Node('param_list', [p[1], p[3]])
    else:
        p[0] = Node('param_list', [p[1]])

def p_parameter(p):
    '''
    parameter : type ID
              | empty
    '''
    if len(p) == 3:
        p[0] = Node('parameter', [p[1]], p[2])
    else:
        p[0] = Node('parameter', [p[1]])

def p_brack_stmt(p):
    '''
    brack_stmt : LBRACE stmts RBRACE
    '''
    p[0] = Node('brack_stmt', [p[2]])
    
def p_stmts(p):
    '''
    stmts : stmts stmt
            | stmt
            | brack_stmt
    '''
    if len(p) == 3:
        p[0] = Node('stmts', [p[1], p[2]])
    else:
        p[0] = Node('stmts', [p[1]])

def p_stmt(p):
    '''
    stmt : expression_stmt
         | ifelse_stmt
         | loop_stmt
         | jump_stmt
    '''
    p[0] = Node('stmt', [p[1]])

def p_expression_stmt(p):
    '''
    expression_stmt : expression SEMICOLON
    '''
    p[0] = Node('expression_stmt', [p[1]])
    
def p_expression(p):
    '''
    expression : assignment_expr
               | empty
    '''
    p[0] = Node('expression', [p[1]])
    
def p_assignment_expr(p):
    '''
    assignment_expr : FUNCT ID ASSIGN LBRACE funct_name COMMA LPAREN reserved_languages_list RPAREN COMMA primary_expr RBRACE
    				| type ID ASSIGN assignment_expr
                    | ID ASSIGN assignment_expr
                    | logical_OR_expr
    '''
    if len(p) == 13:
        p[0] = Node('assignment_expr',  [p[5], p[8], p[11]], p[2])
    elif len(p) == 5:
        p[0] = Node('assignment_expr', [p[1], p[4]], p[2])
    elif len(p) == 4:
        p[0] = Node('assignment_expr', [p[3]], p[1])
    else:
        p[0] = Node('assignment_expr', [p[1]])

def p_funct_name(p):
    '''
    funct_name : __MAIN__
                | ID
    '''
    p[0] = Node('funct_name', [], p[1])

def p_logical_OR_expr(p):
    '''
    logical_OR_expr : logical_AND_expr
                    | logical_OR_expr OR logical_AND_expr    
    '''
    if len(p) == 2:
        p[0] = Node('logical_OR_expr', [p[1]])
    else:
        p[0] = Node('logical_OR_expr', [p[1], p[3]], p[2])
    
def p_logical_AND_expr(p):
    '''
    logical_AND_expr : equality_expr
                     | logical_AND_expr AND equality_expr
    '''
    if len(p) == 2:
        p[0] = Node('logical_AND_expr', [p[1]])
    else:
        p[0] = Node('logical_AND_expr', [p[1], p[3]], p[2])

def p_equality_expr(p):
    '''
    equality_expr : relational_expr
                  | equality_expr EQ relational_expr
                  | equality_expr NEQ relational_expr
    '''
    if len(p) == 2:
        p[0] = Node('equality_expr', [p[1]])
    else:
        p[0] = Node('equality_expr', [p[1], p[3]], p[2])

def p_relational_expr(p):
    '''
    relational_expr : additive_expr
                    | relational_expr LS_OP additive_expr
                    | relational_expr LE_OP additive_expr
                    | relational_expr GR_OP additive_expr
                    | relational_expr GE_OP additive_expr
    '''
    if len(p) == 2:
        p[0] = Node('relational_expr', [p[1]])
    else:
        p[0] = Node('relational_expr', [p[1], p[3]], p[2])
    
def p_additive_expr(p):
    '''
    additive_expr : multiplicative_expr
                  | additive_expr PLUS multiplicative_expr
                  | additive_expr MINUS multiplicative_expr
    '''
    if len(p) == 2:
        p[0] = Node('additive_expr', [p[1]])
    else:
        p[0] = Node('additive_expr', [p[1], p[3]], p[2])
        
def p_multiplicative_expr(p):
    '''
    multiplicative_expr : secondary_expr
                        | multiplicative_expr TIMES secondary_expr
                        | multiplicative_expr DIVIDE secondary_expr
    '''
    if len(p) == 2:
        p[0] = Node('multiplicative_expr', [p[1]])
    else:
        p[0] = Node('multiplicative_expr', [p[1], p[3]], p[2])
    
def p_secondary_expr(p):
    '''
    secondary_expr : primary_expr
                   | LPAREN reserved_languages_list RPAREN
                   | LPAREN expression RPAREN
                   | LBRACE identifier_list RBRACE
    '''
    if len(p) == 4:
        p[0] = Node('secondary_expr', [p[2]])
    else:
        p[0] = Node('secondary_expr', [p[1]])

def p_primary_expr(p):
    '''
    primary_expr : ID
                 | STRINGLITERAL
                 | NUMBER
                 | TRUE
                 | FALSE
                 | function_call
    '''
    if not isinstance(p[1], basestring) and not isinstance(p[1], int) and not isinstance(p[1], float) and not isinstance(p[1], bool):
        p[0] = Node('primary_expr', [p[1]])
    elif len(p) == 2:
        p[0] = Node('primary_expr', [], p[1])
    else:
        p[0] = Node('primary_expr', [p[2]])

def p_function_call(p):
    '''
    function_call : ID LPAREN identifier_list RPAREN
                  | PRINT primary_expr
                  | ID PERIOD ASSERT LPAREN identifier_list RPAREN
    '''
    if len(p) == 3: # PRINT primary_expr
        p[0] = Node('function_call', [p[2]], 'print')
    elif len(p) == 7:
        p[0] = Node('function_call', [Node('ASSERT', [], 'assert'), p[5]], p[1])
    else:
        p[0] = Node('function_call',[p[3]], p[1])
    
def p_reserved_languages_list(p):
    '''
    reserved_languages_list : reserved_language_keyword
                            | reserved_languages_list COMMA reserved_language_keyword
    '''
    if len(p) == 2:
        p[0] = Node('reserved_languages_list', [p[1]])
    else:
        p[0] = Node('reserved_languages_list', [p[1], p[3]])

def p_reserved_language_keyword(p):
    '''
    reserved_language_keyword : RES_LANG LBRACKET RBRACKET
    						  | RES_LANG
                              | empty
    '''
    p[0] = Node('reserved_languages_keyword', [p[1]])
    # TODO: arrays

def p_identifier_list(p):
    '''
    identifier_list : expression
                    | identifier_list COMMA expression
    '''
    if len(p) == 2:
        p[0] = Node('identifier_list', [p[1]])
    else:
        p[0] = Node('identifier_list', [p[1], p[3]])
    
def p_ifelse_stmt(p):
    '''
    ifelse_stmt : IF LPAREN expression RPAREN brack_stmt
                | IF LPAREN expression RPAREN brack_stmt ELSE brack_stmt
    '''
    if len(p) == 6:
        p[0] = Node('ifelse_stmt', [p[3], p[5]])
    else:
        p[0] = Node('ifelse_stmt', [p[3], p[5], p[7]])

def p_loop_stmt(p):
    '''
    loop_stmt : WHILE LPAREN expression RPAREN brack_stmt
              | FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN brack_stmt
    '''
    if len(p) == 6:
        p[0] = Node('loop_stmt', [p[3], p[5]])
    else:
        p[0] = Node('loop_stmt', [p[3], p[5], p[7]])

def p_jump_stmt(p):
    '''
    jump_stmt : BREAK SEMICOLON
              | CONTINUE SEMICOLON
              | RETURN expression SEMICOLON
    '''
    if len(p) == 3:
        p[0] = Node('jump_stmt', [], p[1])
    else:
        p[0] = Node('jump_stmt', [p[2]], p[1])
    
def p_empty(p):
    'empty :'
    p[0] = Node('empty', [])

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
