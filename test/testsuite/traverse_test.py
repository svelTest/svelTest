import unittest
import sys
from testSuite2 import Testsuite

sys.path.append('../../lib')

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

if __name__ == "__main__":
	unittest.main(verbosity =2)