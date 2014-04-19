# =============================================================================
# svelCompile.py
# 
# Main compiler for svelTest programs
#     Input:  A svelTest program (<file_to_compile>.svel)
#     Usage:  python svelCompile.py <file_to_compile>.svel
#     Output: A file named <file_to_compile>.py
# NOTE: If <file_to_compile>.py already exists, compiler does not overwrite
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

import os, sys

# path to ply-3.4
lib_path = os.path.join('ply-3.4')
sys.path.append(lib_path)

from svelLex import SvelLexer
import ply.lex as lex
from node import Node
import svelYacc
import ply.yacc as yacc
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


	# get and build lexer; errorlog=lex.NullLogger() removes PLY warnings
	svel = SvelLexer()
	svel.build(errorlog=lex.NullLogger())

	# get parser; errorlog=yacc.NullLogger() removes PLY warnings
	parser = svelYacc.getParser(errorlog=yacc.NullLogger())

	# parse the data into an abstract syntax tree
	ast = parser.parse(source_code, lexer=svel.get_lexer())

	# walk the tree and get the compiled code
	compiled_code = SvelTraverse(ast).get_code()

	# set the name of the compiled code file
	# e.g. if they compiled helloworld.svel, they'll get helloworld.py
	output_filename = input_filename + ".py"

	# try to write compiled code to appropriate file
	# refuse to overwrite existing file by same name
	if(not os.path.isfile(output_filename)):
		output_file = open(output_filename, 'w')
		output_file.write(compiled_code)
		print "Success: compiled to " + output_filename
	else:
		sys.exit("Error: Refusing to overwrite " + output_filename + "\nPlease either delete it or rename your source file")

if __name__ == '__main__':
	compile(sys.argv)
