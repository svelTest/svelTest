class SvelTraverse(object):

	def __init__(self, tree):
		self.code = self.walk(tree)

	# helper methods to do things...

	def walk(self, tree, flags=None):

		if isinstance(tree, list):
			for item in tree:
				walk(item, flags)
			return

		method = getattr(self, '_'+tree.type)
		return method(tree, flags)

	def get_code(self):
		return self.code

	# traverse methods for specific structures...
	def _main_stmt(self, tree, flags=None):
		print "main_stmt"
		return self.walk(tree.children[0])

	def _print_stmt(self, tree, flags=None):
		print "print_stmt"
		return "print " + self.walk(tree.children[0])

	def _STRINGLITERAL(self, tree, flags=None):
		print "STRINGLITERAL"
		return tree.leaf
