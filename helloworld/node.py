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
		#print "traversing..."
		s = self.type
		indent = "\n" + i*' |'
		if self.leaf != None:
			#print "self.leaf != None..."
			if isinstance(self.leaf, Node):
				print "Node"
				s += indent + self.leaf.traverse(i+1)
			else:
				#print "not Node"
				s += indent + str(self.leaf)
		for children in self.children:
			#print "traversing children..."
			#print str(type(children))
			s += indent + children.traverse(i+1)
		return s

	def __str__(self):
		return self.traverse(1)