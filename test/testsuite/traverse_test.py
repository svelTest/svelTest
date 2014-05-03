import unittest
import os, sys
from testSuite2 import Testsuite

lib_path = os.path.abspath('../../lib')
sys.path.append(lib_path)
#print str(sys.path)
#sys.path.append('../../lib')

import svelYacc
from svelLex import SvelLexer
from svelTraverse import SvelTraverse

class Traverse(unittest.TestCase):

	def setUp(self):
		self.lex = SvelLexer()
		self.lex.build()
		self.lexer = self.lex.get_lexer()

		self.parser = svelYacc.getParser()

	def test_hello(self):
		ast = self.parser.parse(Testsuite.hello_world, lexer=self.lexer)
		code = SvelTraverse(ast).get_code_and_errors()
		print code

	def test_comments(self):
		ast = self.parser.parse(Testsuite.comments, lexer =self.lexer)
		code = SvelTraverse(ast).get_code_and_errors()
		print code

	'''
	def test_empty(self):
		ast = self.parser.parse(Testsuite.empty, lexer = self.lexer)
		code = SvelTraverse(ast).get_code_and_errors()
		print code
	'''

	def test_assignments(self):
		ast = self.parser.parse(Testsuite.assignments, lexer = self.lexer)
		code = SvelTraverse(ast).get_code_and_errors()
		print code

	def test_boolean(self):
		ast = self.parser.parse(Testsuite.expressions_boolean, lexer = self.lexer)
		code = SvelTraverse(ast).get_code_and_errors()
		print code

if __name__ == "__main__":
	unittest.main(verbosity =2)
