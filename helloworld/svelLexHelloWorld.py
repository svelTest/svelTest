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
		'main' : 'MAIN',
		'print' : 'PRINT',
		'file' : 'FILE',
		'if' : 'IF',
		'else' : 'ELSE',
		'assert' : 'ASSERT',
	}

	# Lists of token names. always required
	tokens = [
		'STRINGLITERAL',
		'COMMENT',
		'LPAREN',
		'RPAREN',
		'SEMICOLON',
		'LBRACE',
		'RBRACE',
		'ID',
		'ASSIGN',
		'PERIOD',
	] + list(reserved.values())

	# reg exps for simple tokens must be of form t_TOKENNAME
	t_LPAREN	= r'\('
	t_RPAREN	= r'\)'
	t_SEMICOLON 	= r';'
	t_LBRACE 	= r'{'
	t_RBRACE 	= r'}'
	t_ASSIGN = r'='
	t_PERIOD = r'\.'

	def t_ID(self, t):
		r'[a-zA-Z_][a-zA-Z0-9_]*'
		# searches reserved for t.value
		# 	if found, sets t.type to t.VALUE 
		# 	otherwise sets t.type to ID
		t.type = self.reserved.get(t.value, 'ID')
		return t

	def t_STRINGLITERAL(self, t):
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
