import unittest
import os, sys
from testSuite2 import Testsuite

lib_path = os.path.abspath('../../lib')
sys.path.append(lib_path)

import svelYacc
from svelLex import SvelLexer


class Yacc(unittest.TestCase):

	def setUp(self):
		self.lex = SvelLexer()
		self.lex.build()
		self.lexer = self.lex.get_lexer()
	
		self.parser = svelYacc.getParser()

	def test_hello(self):
		code = self.parser.parse(Testsuite.hello_world)
		print code

	def test_comments(self):
		code = self.parser.parse(Testsuite.comments)
		print code

	def test_empty(self):
		code = self.parser.parse(Testsuite.empty)
		print code

	def test_assingments(self):
		code = self.parser.parse(Testsuite.assignments)
		print code

	def test_boolean(self):
		code = self.parser.parse(Testsuite.expressions_boolean)
		print code


if __name__ == "__main__":
	unittest.main(verbosity =2)
