import unittest
import sys
from testSuite2 import Testsuite

sys.path.append('../../lib')

import svelYacc
from svelTraverse import SvelTraverse





class Traverse(unitTest.TestCase):

	def setUp(self):
		self.parser = svelYacc.getParser

	def hello_test(self):
		result = self.parser.parse(Testsuite.hello_world)
		translated = SvelTraverse(result).getpython()
		print translated

if __name__ == "__main__":
	unittest.main(verbosity =2)
