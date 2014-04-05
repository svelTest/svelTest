class SvelTraverse(object):

	def __init__(self, tree):
		self.level = 0
		self.code = self.walk(tree) + self.end()

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

		line += self.walk(tree.children[0])
		
		# leave scope
		self.level_down()
		return line

	def _print_stmt(self, tree, flags=None):
		line = "print "
		line = self.format(line)
		return line + self.walk(tree.children[0]) + '\n'

	def _STRINGLITERAL(self, tree, flags=None):
		return tree.leaf