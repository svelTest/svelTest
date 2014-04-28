# =============================================================================
# node.py
# 
# Node class represents a node of the abstract syntax tree
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

class Node(object):

	def __init__(self, type, children=None, leaf=None, token=None, lineno=None):
		self.type = type
		if children:
			self.children = children
		else:
			self.children = []
		self.leaf = leaf
		self.token = token
		self.lineno = lineno

	def traverse(self, i):
		s = self.type
		indent = "\n" + i*' |'
		if self.leaf != None:
			if isinstance(self.leaf, Node):
				s += indent + self.leaf.traverse(i+1)
			else:
				s += indent + str(self.leaf)
		for child in self.children:
			if isinstance(child, basestring):
				print child
			s += indent + child.traverse(i+1)
		return s

	def __str__(self):
		return self.traverse(1)