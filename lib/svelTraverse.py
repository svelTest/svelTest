class SvelTraverse(object):

	def __init__(self, tree):
		self.level = 0
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
		return "\nif __name__ == '__main__': \n    main()"

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
		return self.walk(tree.children[0])

	# TODO: handle non-main fcns; parameter list with multiple parameters
	def _function_def(self, tree, flags=None):
		print "===> svelTraverse: function_def"
		if len(tree.children) == 2: # main

			# TODO: use the format function to do indenting
			line = "def main("
			line += self.walk(tree.children[0])
			line += "):\n    "
			line += self.walk(tree.children[1])
			return line
			
		elif tree.children[0].leaf == "VOID": # return void
			print "returns VOID"
		else: # function returning a type
			print "returns" + tree.children[0].leaf

		return self.walk(tree.children[1])

	# TODO: go through entire parameter list
	def _param_list(self, tree, flags=None):
		print "===> svelTraverse: param_list"
		return self.walk(tree.children[0])

	def _parameter(self, tree, flags=None):
		print "===> svelTraverse: parameter"
		return self.walk(tree.children[0])

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
		return self.walk(tree.children[0])

	def _stmt(self, tree, flags=None):
		print "===> svelTraverse: stmt"
		return self.walk(tree.children[0])

	# expressions...
	def _expression_stmt(self, tree, flags=None):
		print "===> svelTraverse: expression_stmt"
		return self.walk(tree.children[0])

	def _expression(self, tree, flags=None):
		print "===> svelTraverse: expression"
		return self.walk(tree.children[0])

	def _assignment_expr(self, tree, flags=None):
		print "===> svelTraverse: assignment_expr"
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
		return self.walk(tree.children[0])

	def _function_call(self, tree, flags=None):
		print "===> svelTraverse: function_call"
		if tree.leaf == "print":
			return tree.leaf + " " + tree.children[0].leaf

	'''
		TODO: add methods for these...
			reslang_type
			reserved_languages_list
			reserved_language_keyword
			identifier_list
			ifelse_stmt
			loop_stmt
			jump_stmt
			funct_name
	'''

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

	def _brack_stmt(self, tree, flags=None):
		line = self.walk(tree.children[0])
		line = self.format(line)
		return line

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