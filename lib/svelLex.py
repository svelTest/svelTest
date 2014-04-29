# =============================================================================
# svelLex.py
#
# Tokenizer for svelTest programs: takes an input data stream and tokenizes it
# 
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

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
		'int' : 'INT',
		'double' : 'DOUBLE',
		'char' : 'CHAR',
		'string' : 'STRING',
		'funct' : 'FUNCT',
		'output' : 'OUTPUT',
		'input' : 'INPUT',
		'file' : 'FILE',
		'main' : 'MAIN',
		'__main__' : '__MAIN__',
		'boolean' : 'BOOLEAN',
		'if' : 'IF',
		'else' : 'ELSE',
		'while' : 'WHILE',
		'for' : 'FOR',
		'print' : 'PRINT',
		'true' : 'TRUE',
		'false' : 'FALSE',
		'void' : 'VOID',
		'assert' : 'ASSERT',
		'remove' : 'REMOVE',
		'size' : 'SIZE',
		'insert' : 'INSERT',
		'replace' : 'REPLACE',
		'break' : 'BREAK',
		'continue' : 'CONTINUE',
		'return' : 'RETURN',
		'verbose' : 'VERBOSE',
		'lang' : 'LANG',
		'readlines' : 'READLINES',
		# start Python reserved words
		'and' : 'PYTHON_AND',
		'as' : 'AS',
		'class' : 'CLASS',
		'def' : 'DEF',
		'del' : 'DEL',
		'elif' : 'ELIF',
		'except' : 'EXCEPT',
		'exec' : 'EXEC',
		'finally' : 'FINALLY',
		'from' : 'FROM',
		'global' : 'GLOBAL',
		'import' : 'IMPORT',
		'in' : 'IN',
		'is' : 'IS',
		'lambda' : 'LAMBDA',
		'not' : 'NOT',
		'or' : 'PYTHON_OR',
		'pass' : 'PASS',
		'raise' : 'RAISE',
		'try' : 'TRY',
		'with' : 'WITH',
		'yield' : 'YIELD',
	}

	# Lists of token names. always required
	tokens = [
		'RES_LANG',
		'ID',
		'NUMBER',
		'DECIMAL',
		'STRINGLITERAL',
		'COMMENT',
		'PLUS',
		'MINUS',
		'TIMES',
		'DIVIDE',
		'LPAREN',
		'RPAREN',
		'ASSIGN',
		'SEMICOLON',
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
	t_STRING 	= r'"(\\.|[^"])*"'
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
	def t_RES_LANG(self, t):
		r'''
		j_int|j_double|j_float|j_byte|j_char|j_String|j_boolean|j_long
		|c_char|c_signed_char|c_unsigned_char|c_short|c_short_int|c_signed_short
		|c_signed_short_int|c_unsigned_short|c_unsigned_short_int|c_int|c_signed_short_int
		|c_long|c_long_int|c_signed_long|c_signed_long_int|c_unsigned_long
		|c_unsigned_long_int|c_long_long|c_long_long_int|c_signed_long_long
		|c_signed_long_long_int|c_unsigned_long_long|c_unsigned_long_long_int
		|c_float|c_double|c_long_double|p_int|p_bool|p_long|p_float|p_str'''
		t.type = 'RES_LANG'
		return t

	def t_ID(self, t):
		r'[a-zA-Z_][a-zA-Z0-9_]*'
		# searches reserved for t.value
		# 	if found, sets t.type to t.VALUE 
		# 	otherwise sets t.type to ID
		t.type = self.reserved.get(t.value, 'ID')
		return t

	def t_DECIMAL(self, t):
		r'-?\d+\.\d*'
		t.value = float(t.value)
		return t

	def t_NUMBER(self, t):
		r'-?\d+'
		t.value = int(t.value)
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


# if svelLex.py invoked directly, tokenize user's input
if __name__ == "__main__":
	# instantiate new svelLexer
	svel = SvelLexer()

	# build the lexer
	svel.build()

	# if user just ran "python svelLex.py", start input loop
	if(len(sys.argv) == 1):
 
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

	# otherwise, try to read user's file (e.g. they ran something like
	# "python svelLex.py helloworld.svel")
	else:
		# try to open the file
		try:
			data = open(sys.argv[1]).read()
		except IOERROR, e:
			print e

		# tokenize the file
		print svel.tok_str(data)