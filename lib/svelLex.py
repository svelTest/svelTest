# ---------------------------------------------------------
# svelLex.py
#
# tokenizer for svelTest programs
# ---------------------------------------------------------

# be able to go into the ply directory to get to the 
# ply modules
import os, sys
lib_path = os.path.join('ply-3.4')
sys.path.append(lib_path)

# import ply (imports from ply-3.4/ply)
import ply.lex as lex

# define svelLex class
class SvelLexer: 
	# set up reserved words
	reserved = {
		'import' : 'IMPORT',
		'test' : 'TEST',
		'int' : 'INT',
		'function' : 'FUNCTION',
		'param' : 'PARAM',
		'output' : 'OUTPUT',
		'testcase' : 'TESTCASE',
		'sysout' : 'SYSOUT',
		'main' : 'MAIN',
		'boolean' : 'BOOLEAN',
		'if' : 'IF',
		'else' : 'ELSE',
		'while' : 'WHILE',
		'print' : 'PRINT',
	}
	# Lists of token names. always required
	tokens = [
		'ID',
		'NUMBER',
		'STRING',
		'COMMENT',
		'PLUS',
		'MINUS',
		'TIMES',
		'DIVIDE',
		'LPAREN',
		'RPAREN',
		'ASSIGN',
		'SEMICOLON',
		'COLON',
		'PERIOD',
		'COMMA',
		'LBRACE',
		'RBRACE',
		'LBRACKET',
		'RBRACKET',
		'GR_OP',
		'LS_OP',
		'GE_OP',
		'LE_OP',
		'AND',
		'OR',
		'EQ',
		'NEQ',
	] + list(reserved.values())

	# reg exps for simple tokens must be of form t_TOKENNAME
	t_PLUS 		= r'\+'
	t_MINUS		= r'-'
	t_TIMES		= r'\*'
	t_DIVIDE	= r'/'
	t_LPAREN	= r'\('
	t_RPAREN	= r'\)'
	t_ASSIGN	= r'='
	t_SEMICOLON = r';'
	t_COLON		= r':'
	t_PERIOD	= r'\.'
	t_COMMA		= r','
	t_LBRACE 	= r'{'
	t_RBRACE 	= r'}'
	t_LBRACKET	= r'\['
	t_RBRACKET	= r'\]'
	t_GR_OP		= r'>'
	t_LS_OP		= r'<' 		
	t_GE_OP		= r'>='
	t_LE_OP		= r'<='
	t_AND		= r'&&'
	t_OR 		= r'\|\|'
	t_EQ 		= r'=='
	t_NEQ 		= r'!='

	# reg exp rule with some action code
	def t_ID(self, t):
		r'[a-zA-Z_][a-zA-Z0-9_]*'
		# searches reserved for t.value
		# 	if found, sets t.type to t.VALUE 
		# 	otherwise sets t.type to ID
		t.type = self.reserved.get(t.value, 'ID')
		return t

	def t_NUMBER(self, t):
		r'\d+'
		t.value = int(t.value)
		return t

	def t_STRING(self, t):
		r'"[^"]*"'
		return t

	# regular expression from http://ostermiller.org/findcomment.html
	t_ignore_COMMENT = r'(/\*([^*]|[\n]|(\*+([^*/]|[\n])))*\*+/)|(//.*)'

	# define newline rule to track line numbers
	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	# string containing ignored characters
	t_ignore = ' \t'

	# error handling
	def t_error(self, t):
		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	# build the lexer
	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

	# get the lexer
	def get_lexer(self):
		return self.lexer

	# tokenize a string
	def tok_str(self, data):
		self.lexer.input(data)
		tok_str = ""
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			tok_str += str(tok) + "\n"
		return tok_str


# if svelLex.py invoked directly, tokenize input
if __name__ == "__main__":
	# instantiate new svelLexer
	svel = SvelLexer()

	# build the lexer
	svel.build()
 
 	# loop to get user input
	while True:
		# print prompt and gather input
		try:
			line = raw_input("Enter a string to tokenize\n")

		# if Ctrl-D, exit
		except EOFError:
			break

		# otherwise, tokenize the string
		print svel.tok_str(line)