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

def p_main_function(p):
	'''
	main_function : MAIN LPAREN RPAREN LBRACE statements RBRACE
	'''
	p[0] = "main() \n{ " + p[5] + " \n}"

def p_statements(p):
	'''
	statements : statement statements
			   | statement
	'''
	if len(p) == 3:
		p[0] = p[1]
	else:
		p[0] = p[1]

def p_statement(p):
	'''
	statement : TESTCASE variable ASSIGN LBRACE variable COMMA variable RBRACE SEMICOLON
	'''
	p[0] = "testcase " + p[2] + " ={ " + p[5] + " , " + p[7] + " };"

def p_variable(p):
	'''
	variable : ID
	'''
	p[0] = p[1]

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
		print parser.parse(data, lexer=svel.get_lexer())