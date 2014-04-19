# =============================================================================
# testParser.py
# 
# Runs testsuite test cases on parser
# Usage: python testParser.py [test case #]*
#    python testParser.py: will run all test cases
#    python testParser.py x: will run test case x
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

# get to lib for svelLex file
import os, sys
lib_path = os.path.join('../lib')
sys.path.append(lib_path)

# get to ply
lib_path = os.path.join('../lib/ply-3.4')
sys.path.append(lib_path)

# import lexer class
from svelLex import SvelLexer

# import parser
import svelYacc

# get and build lexer
svel = SvelLexer()
svel.build()

# get parser
parser = svelYacc.getParser()

from testsuite import Testsuite
ts = Testsuite()

# If run with no arguments -- test all cases in testsuite
# $ python testSvelYacc.py
if len(sys.argv) == 1:
	cases = ts.getAll()
	i = 0;
	for case in cases:
		print 80*'='
		print '#%d test code: \n %s \n' % (i, case)
		print parser.parse(case, lexer=svel.get_lexer())
		i = i + 1

# If run with arguments -- test those case numbers in testsuite
# $ python testSvelYacc.py 0 3
else:
	i = 1;
	while i < len(sys.argv):
		case = ts.get(int(sys.argv[i]))
		print 80*'='
		print '#%s test code: \n %s \n' % (sys.argv[i], case)
		print parser.parse(case, lexer=svel.get_lexer())
		i = i + 1