# ---------------------------------------------------------
# calclex.py
#
# tokenizer for simple expression evaluator for numbers
# and +,-,*,/
#
# from www.dabeaz.com/ply/ply.html
# ---------------------------------------------------------

# be able to go into the ply directory to get to the 
# ply modules
import os, sys
lib_path = os.path.join('ply-3.4')
sys.path.append(lib_path)

# import ply (imports from ply-3.4/ply)
import ply.lex as lex

# Lists of token names. always required
tokens = (
	'NUMBER',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'LPAREN',
	'RPAREN',
)

# reg exps for simple tokens
# must be of form t_TOKENNAME
t_PLUS 		= r'\+'
t_MINUS		= r'\-'
t_TIMES		= r'\*'
t_DIVIDE	= r'/'
t_LPAREN	= r'\('
t_RPAREN	= r'\)'

# reg exp rule with some action code
def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

# define newline rule to track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# string containing ignored characters
t_ignore = ' \t'

# error handling
def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

# build lexer
lexer = lex.lex()

# give lexer some data
data = '''
3 + 4 * 10
  + -20 * 2
'''

# give lexer input
lexer.input(data)

# tokenize
while True:
	tok = lexer.token()
	if not tok: break		# no more input
	print tok 