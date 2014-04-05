# =============================================================================
# Main compiler
# Usage: python svelCompile.py <file_to_compile>.svel
#
# Output: A file named <file_to_compile>.py
# NOTE: If <file_to_compile>.py already exists, compiler does not overwrite
# =============================================================================

import os, sys
lib_path = os.path.join('ply-3.4')
sys.path.append(lib_path)

from svelLexHelloWorld import SvelLexer
from node import Node
import svelYaccHelloWorld
from svelTraverse import SvelTraverse

def compile(argv):
	# TODO: else if no arguments provided
	if len(argv) == 2:
		input_file = argv[1]
	else:
		sys.exit("Usage: python svelCompile.py <file_to_compile>.svel")

	# get name of input file to use later
	input_filename = input_file.split(".")[0]

	# try to open source code
	try:
		source_code = open(input_file).read()
	except IOERROR, e:
		print e


	# get and build lexer
	svel = SvelLexer()
	svel.build()

	# get parser
	parser = svelYaccHelloWorld.getParser()

	# parse the data into an abstract syntax tree
	ast = parser.parse(source_code, lexer=svel.get_lexer())

	# walk the tree and get the compiled code
	compiled_code = SvelTraverse(ast).get_code()

	# set the name of the compiled code file
	# e.g. if they compiled helloworld.svel, they'll get helloworld.py
	code_file = input_filename + ".py"

	# try to write compiled code to appropriate file
	# refuse to overwrite existing file by same name
	if(not os.path.isfile(code_file)):
		output = open(code_file, 'w')
		output.write(compiled_code)
	else:
		sys.exit("Error: Refusing to overwrite " + code_file + "\nPlease either delete it or rename your source file")

if __name__ == '__main__':
	compile(sys.argv)