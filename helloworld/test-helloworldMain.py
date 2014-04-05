
import os, sys
lib_path = os.path.join('ply-3.4')
sys.path.append(lib_path)

from svelLexHelloWorld import SvelLexer
import ply.lex as lex
from node import Node
import svelYaccHelloWorld
import ply.yacc as yacc
from svelTraverse import SvelTraverse


# get and build lexer; errorlog=lex.NullLogger() removes PLY warnings
svel = SvelLexer()
svel.build(errorlog=lex.NullLogger())


data = '''
// tries to run a python file and test output

main() {
	file helloFile = "printhelloworld.py";

	// I know this isn't real syntax, just trying shit out
	if(helloFile.assert) {
		print "Hello World passed.";
	} else {
		print "Hello World failed.";
	}
}
'''
#print svel.tok_str(data)

# get parser; errorlog=yacc.NullLogger() removes PLY warnings
parser = svelYaccHelloWorld.getParser(errorlog=yacc.NullLogger())

# parse the data into an abstract syntax tree
ast = parser.parse(data, lexer=svel.get_lexer())

compiled_code = SvelTraverse(ast).get_code()

output_filename = "test.py"
output_file = open(output_filename, 'w')
output_file.write(compiled_code)