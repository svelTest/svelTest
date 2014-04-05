class Node(object):

	def __init__(self, type, children=None, leaf=None, token=None):
		self.type = type
		if children:
			self.children = children
		else:
			self.children = []
		self.leaf = leaf
		self.token = token

	def traverse(self, i):
		s = self.type
		indent = "\n" + i*' |'
		if self.leaf != None:
			if isinstance(self.leaf, Node):
				print "Node"
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