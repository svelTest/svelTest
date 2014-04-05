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
		return "if __name__ == '__main__': \n    main()"

	# --------------------
	# handle grammar nodes
	# --------------------

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