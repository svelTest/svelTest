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
		return "import os, sys\n"

	def end(self):
		return "\nif __name__ == '__main__':\n    main()"

	# --------------------
	# handle grammar nodes
	# --------------------

	# so far it only works for test/hello.svel example

	# TODO: handle else case (see grammar)
	def _translation_unit(self, tree, flags=None):
		print "===> svelTraverse: translation_unit"
		if len(tree.children) == 1:
			return self.walk(tree.children[0])
		elif len(tree.children) == 2:
			return self.walk(tree.children[0]) + "\n" + self.walk(tree.children[1])

	# TODO: handle else case (see grammar)
	def _external_declaration(self, tree, flags=None):
		print "===> svelTraverse: external_declaration"

		# if function_def
		if tree.leaf == None:
			return self.walk(tree.children[0])

		# if external var declaration
		else:
			return ""
			#return self.walk(tree.children[0]) + " " + tree.leaf

	# TODO: handle non-main fcns; parameter list with multiple parameters
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

	# TODO: go through entire parameter list
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
		return self.walk(tree.children[0])

	def _logical_AND_expr(self, tree, flags=None):
		print "===> svelTraverse: logical_AND_expr"
		return self.walk(tree.children[0])

	def _equality_expr(self, tree, flags=None):
		print "===> svelTraverse: equality_expr"
		return self.walk(tree.children[0])

	def _relational_expr(self, tree, flags=None):
		print "===> svelTraverse: relational_expr"
		return self.walk(tree.children[0])

	def _additive_expr(self, tree, flags=None):
		print "===> svelTraverse: additive_expr"
		return self.walk(tree.children[0])

	def _multiplicative_expr(self, tree, flags=None):
		print "===> svelTraverse: multiplicative_expr"
		return self.walk(tree.children[0])

	def _secondary_expr(self, tree, flags=None):
		print "===> svelTraverse: secondary_expr"
		return self.walk(tree.children[0])

	def _primary_expr(self, tree, flags=None):
		print "===> svelTraverse: primary_expr"

		if len(tree.children) == 0:
			# is ID or function_call?
			return tree.leaf

		return self.walk(tree.children[0])

	def _function_call(self, tree, flags=None):
		print "===> svelTraverse: function_call"

		line = ""
		if tree.leaf == "print":
			line += tree.leaf + " " + tree.children[0].leaf

		return line

	def _reslang_type(self, tree, flags=None):
		print "===> svelTraverse: reslang_type"
		return self.walk(tree.children[0])

	def _reserved_languages_list(self, tree, flags=None):
		print "===> svelTraverse: reserved_languages_list"
		return self.walk(tree.children[0])

	def _reserved_languages_keyword(self, tree, flags=None):
		print "===> svelTraverse: _reserved_languages_keyword"
		return self.walk(tree.children[0])

	def _identifier_list(self, tree, flags=None):
		print "===> svelTraverse: _identifier_list"
		return self.walk(tree.children[0])

	def _ifelse_stmt(self, tree, flags=None):
		print "===> svelTraverse: _ifelse_stmt"
		return self.walk(tree.children[0])

	def _loop_stmt(self, tree, flags=None):
		print "===> svelTraverse: _loop_stmt"
		return self.walk(tree.children[0])

	def _jump_stmt(self, tree, flags=None):
		print "===> svelTraverse: _jump_stmt"
		return self.walk(tree.children[0])

	def _funct_name(self, tree, flags=None):
		print "===> svelTraverse: _funct_name"
		return self.walk(tree.children[0])

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