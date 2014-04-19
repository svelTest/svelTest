class SvelTraverse(object):

	def __init__(self, tree):

		# scope/indentation level
		self.level = 0

		# symbol table (dict)
		self.symbols = {}

		# value table (dict)
		self.values = {}

		# run
		self.code = self.beginning() + self.walk(tree) + self.end()

	# --------------
	# helper methods
	# --------------

	def walk(self, tree, flags=None):
		''' call appropriate method based on node type '''
		if isinstance(tree, list):
			for item in tree:
				walk(item, flags)
			return

		method = getattr(self, '_'+tree.type)
		return method(tree, flags)

	def get_code(self):
		return self.code

	def format(self, line = ""):
		''' indent a line according to its level '''
		spaces = 4 * self.level
		return " "*spaces + line

	def level_up(self):
		''' +1 indent; TODO: create new scope '''
		self.level += 1

	def level_down(self):
		''' -1 indent; TODO: remove old scope '''
		self.level -= 1

	def beginning(self):
		return "import os, sys\nfrom funct import Funct\n\n"

	def end(self):
		return "\n\nif __name__ == '__main__':\n    main()"

	# --------------------
	# handle grammar nodes
	# --------------------

	# passes testsuite tests 0, 1, 2, 3, 5, 8; works for hello.svel

	# TODO: make sure that we return and are concatenating string types

	def _translation_unit(self, tree, flags=None):
		print "===> svelTraverse: translation_unit"
		if len(tree.children) == 1:
			return self.walk(tree.children[0])
		elif len(tree.children) == 2:
			return self.walk(tree.children[0]) + "\n\n" + self.walk(tree.children[1])

	def _external_declaration(self, tree, flags=None):
		print "===> svelTraverse: external_declaration"

		# if function_def
		if tree.leaf == None:
			return self.walk(tree.children[0])

		# if external var declaration
		else:
			return ""
			#return self.walk(tree.children[0]) + " " + tree.leaf

	def _function_def(self, tree, flags=None):
		print "===> svelTraverse: function_def"

		# TODO: use the format function to do indenting
		if len(tree.children) == 2: # main
			line = "def main("
			line += self.walk(tree.children[0])
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[1])

			self.level_down()

		elif tree.children[0].leaf == "VOID":
			# TODO: do something with the return type?
			print "returns VOID"
			line = "def "
			line += tree.leaf
			line += "("
			line += self.walk(tree.children[1])
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[2])
			self.level_down()

		else: # function returning a type
			# TODO: do something with the return type?
			# type is in tree.children[0]
			print "returns" + tree.children[0].leaf
			line = "def "
			line += tree.leaf
			line += "("
			line += self.walk(tree.children[1])
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[2])
			self.level_down()

		return line

	def _param_list(self, tree, flags=None):
		print "===> svelTraverse: param_list"

		line = ""

		# if there's another parameter
		if len(tree.children) == 2:
			line += self.walk(tree.children[0])
			line += ', '
			line += self.walk(tree.children[1])

		else: # last parameter in list
			line += self.walk(tree.children[0])

		return line

	def _parameter(self, tree, flags=None):
		print "===> svelTraverse: parameter"

		# if empty --> _empty
		if tree.leaf == None:
			return self.walk(tree.children[0])

		# TODO: add entry to symbol table
		# type = self.walk(tree.children[0])

		# put ID in code
		return tree.leaf

	def _empty(self, tree, flags=None):
		print "===> svelTraverse: empty"
		return ""

	def _type(self, tree, flags=None):
		print "===> svelTraverse: type"
		return tree.leaf

	def _brack_stmt(self, tree, flags=None):
		print "===> svelTraverse: brack_stmt"
		return self.walk(tree.children[0])

	def _stmts(self, tree, flags=None):
		print "===> svelTraverse: stmts"

		line = ""
		if len(tree.children) == 2:
			# consecutive stmts
			line += self.walk(tree.children[0])
			line += '\n'
			line += self.walk(tree.children[1])

		else:
			# stmt or brack_stmt
			line += self.walk(tree.children[0])

		return line

	def _stmt(self, tree, flags=None):
		print "===> svelTraverse: stmt"
		return self.format(self.walk(tree.children[0]))

	# expressions...
	def _expression_stmt(self, tree, flags=None):
		print "===> svelTraverse: expression_stmt"
		return self.walk(tree.children[0])

	def _expression(self, tree, flags=None):
		print "===> svelTraverse: expression"
		return self.walk(tree.children[0])

	def _assignment_expr(self, tree, flags=None):
		print "===> svelTraverse: assignment_expr"

		# TODO: handle FUNCT!
		if tree.leaf == None:
			# logical_OR_expression
			return self.walk(tree.children[0])

		elif len(tree.children) == 3:
			# FUNCT ID ASSIGN LBRACE funct_name COMMA LPAREN reserved_languages_list RPAREN COMMA primary_expr RBRACE
			return tree.leaf + " = Funct(" + self.walk(tree.children[0]) + \
				", " + self.walk(tree.children[1]) + \
				", " + self.walk(tree.children[2]) + ")"

		elif len(tree.children) == 2:
			# initial declaration w/ assignment
			# TODO: do something with the type (symbol table)
			return tree.leaf + " = " + str(self.walk(tree.children[1]))

		elif len(tree.children) == 1:
			# assignment
			return tree.leaf + " = " + str(self.walk(tree.children[0]))


		return self.walk(tree.children[0])

	def _logical_OR_expr(self, tree, flags=None):
		print "===> svelTraverse: logical_OR_expr"

		line = ""
		if len(tree.children) == 2:
			# logical_OR_expr OR logical_AND_expr
			line += str(self.walk(tree.children[0]))
			line += " or "
			line += str(self.walk(tree.children[1]))

		else:
			# go to logical_AND_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _logical_AND_expr(self, tree, flags=None):
		print "===> svelTraverse: logical_AND_expr"

		line = ""
		if len(tree.children) == 2:
			# logical_AND_expr OR equality_expr
			line += str(self.walk(tree.children[0]))
			line += " and "
			line += str(self.walk(tree.children[1]))

		else:
			# go to equality_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _equality_expr(self, tree, flags=None):
		print "===> svelTraverse: equality_expr"

		line = ""
		if len(tree.children) == 2:
			# equality_expr EQ/NEQ relational_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# go to relational_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _relational_expr(self, tree, flags=None):
		print "===> svelTraverse: relational_expr"

		line = ""
		if len(tree.children) == 2:
			# relational_expr LS_OP/LE_OP/GR_OP/GE_OP additive_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# go to additive_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line


	def _additive_expr(self, tree, flags=None):
		print "===> svelTraverse: additive_expr"

		line = ""
		if len(tree.children) == 2:
			# additive_expr PLUS/MINUS multiplicative_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# go to multiplicative_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _multiplicative_expr(self, tree, flags=None):
		print "===> svelTraverse: multiplicative_expr"

		line = ""
		if len(tree.children) == 2:
			# multiplicative_expr TIMES/DIVIDE secondary_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# go to multiplicative_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _secondary_expr(self, tree, flags=None):
		print "===> svelTraverse: secondary_expr"

		line = ""
		if tree.leaf == None:
			# -> primary_expr
			line += str(self.walk(tree.children[0]))

		elif tree.leaf == '(':
			# -> LPAREN expression RPAREN
			line += '(' + str(self.walk(tree.children[0])) + ')'

		elif tree.leaf == '{':
			# -> LBRACE identifier_list RBRACE
			line += '[' + str(self.walk(tree.children[0])) + ']'

		return line

	def _primary_expr(self, tree, flags=None):
		print "===> svelTraverse: primary_expr"

		if len(tree.children) == 0:
			# if not function_call or ref_type
			return tree.leaf

		return self.walk(tree.children[0])

	def _function_call(self, tree, flags=None):
		print "===> svelTraverse: function_call"

		line = ""
		if tree.leaf == "print":
			# -> PRINT primary_expr
			line += tree.leaf + " " + tree.children[0].leaf

		elif len(tree.children) == 2:
			# -> ID PERIOD ASSERT LPAREN identifier_list RPAREN
			line += tree.leaf + ".assert(" + self.walk(tree.children[1]) +")"

		elif len(tree.children) == 1:
			# -> ID LPAREN identifier_list RPAREN
			line += tree.leaf + "(" + self.walk(tree.children[0]) + ")"

		return line

	def _ref_type(self, tree, flags=None):
		print "===> svelTraverse: ref_type"

		line = ""
		line += self.walk(tree.children[0])
		line += '['
		line += str(self.walk(tree.children[1]))
		line += ']'
		return line		

	def _reserved_languages_list(self, tree, flags=None):
		print "===> svelTraverse: reserved_languages_list"
		
		line = ""
		if len(tree.children) == 1:
			# -> reserved_languages_keyword
			line += self.walk(tree.children[0])

		elif len(tree.children) == 2:
			# -> reserved_languages_list COMMA reserved_languages_keyword
			line += self.walk(tree.children[0]) + ", " + self.walk(tree.children[1])

		return line

	def _reserved_languages_keyword(self, tree, flags=None):
		print "===> svelTraverse: reserved_languages_keyword"
		
		if isinstance(tree.leaf, basestring):
			print tree.leaf
			return tree.leaf

		return "[]"

	def _identifier_list(self, tree, flags=None):
		print "===> svelTraverse: _identifier_list"

		line = ""
		if len(tree.children) == 1:
			# -> expression
			line += str(self.walk(tree.children[0]))

		elif len(tree.children) == 2:
			# -> identifier_list COMMA expression
			line += str(self.walk(tree.children[0])) + ", " + str(self.walk(tree.children[1]))

		return line

	def _ifelse_stmt(self, tree, flags=None):
		print "===> svelTraverse: _ifelse_stmt"

		line = ""
		if len(tree.children) == 2:
			# if
			line += "if "
			line += self.walk(tree.children[0])
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1])
			self.level_down()

		elif len(tree.children) == 3:
			# if-else
			line += "if "
			line += self.walk(tree.children[0])
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1]) + "\n"
			self.level_down()

			# need to format this line since it's not the beginning of the stmt
			line += self.format("else:\n")

			self.level_up()
			line += self.walk(tree.children[2])
			self.level_down()

		return line

	def _loop_stmt(self, tree, flags=None):
		print "===> svelTraverse: _loop_stmt"

		line = ""
		if len(tree.children) == 2:
			# while
			line += "while "
			line += self.walk(tree.children[0])
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1])
			self.level_down()

		elif len(tree.children) == 4:
			# for TODO: refactor -- very hack-y atm
			line += self.walk(tree.children[0]) + '\n'
			line += self.format("while ")
			line += self.walk(tree.children[1])
			line += ":\n"

			self.level_up()
			# TODO: insert statements inside the for loop
			line += self.walk(tree.children[3]) + '\n'
			line += self.format(self.walk(tree.children[2]))
			self.level_down()

		return line

	def _jump_stmt(self, tree, flags=None):
		print "===> svelTraverse: _jump_stmt"

		line = ""
		if tree.leaf == 'break':
			line = tree.leaf

		elif tree.leaf == 'continue':
			line = tree.leaf

		elif tree.leaf == 'return':
			line += "return "
			line += self.walk(tree.children[0])

		return line

	def _funct_name(self, tree, flags=None):
		print "===> svelTraverse: _funct_name"
		return tree.leaf

	# -----------------
	# OLD (from helloworld/svelTraverse.py) TODO: delete
	# -----------------

	# TODO: indenting; scoping
	def _main_stmt(self, tree, flags=None):
		line = "def main():"
		line = self.format(line)
		line += '\n'

		# enter scope
		self.level_up()

		if len(tree.children) == 1:
			line += self.walk(tree.children[0])
		else:
			line += self.walk(tree.children[0]) + self.walk(tree.children[1])

		
		# leave scope
		self.level_down()
		return line

	# hardcoding in the comparison for now - iIknow it's wrong
	# just wanted to get something going
	def _if_else_loop(self, tree, flags=None):
		line = "os.system(\"python printhelloworld.py > output.txt\")\n"
		line2 = "output = open(\"output.txt\").read()\n"
		line3 = "if output == \"Hello, World!\\n\":\n"
		line5 = "else:\n"

		line = self.format(line)
		line2 = self.format(line2)
		line3 = self.format(line3)
		line5 = self.format(line5)

		self.level_up()

		line4 = self.walk(tree.children[1])
		line6 = self.walk(tree.children[2])

		self.level_down()

		return line + line2 + line3 + line4 + line5 + line6


	def _print_stmt(self, tree, flags=None):
		line = "print "
		line = self.format(line)
		return line + self.walk(tree.children[0]) + '\n'

	'''
	def _brack_stmt(self, tree, flags=None):
		line = self.walk(tree.children[0])
		line = self.format(line)
		return line
	'''

	def _file_stmt(self, tree, flags=None):
		line = "if(not os.path.isfile("
		line = self.format(line)
		line += self.walk(tree.children[1]) + ")):\n"
		
		next_line = "    sys.exit('Cannot find "
		next_line = self.format(next_line)
		next_line += self.walk(tree.children[1]) + "')"

		return line + next_line + '\n'

	def _STRINGLITERAL(self, tree, flags=None):
		return tree.leaf

	def _ID(self, tree, flags=None):
		return tree.leaf