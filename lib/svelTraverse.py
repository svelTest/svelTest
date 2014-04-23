# =============================================================================
# svelTraverse.py
#
# Tree-walker for svelTest programs: takes an abstract syntax tree and 
# attempts to traverse it to produce the target .py program
# 
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================
import sys;
class SvelTraverse(object):

	def __init__(self, tree, verbose=False):

		# scope/indentation level
		self.level = 0

		# symbol table (dict)
		self.symbols = {}

		# scope table (dict)
		self.scopes = [{}]

		# TODO command line args hack
		self.main_args = []
		self.main_types = []

		# run
		self.code = self.beginning() + self.walk(tree, verbose=verbose) + self.end()

	# --------------
	# helper methods
	# --------------

	def walk(self, tree, flags=None, verbose=False):
		''' call appropriate method based on node type '''
		if isinstance(tree, list):
			for item in tree:
				self.walk(item, flags, verbose)
			return

		method = getattr(self, '_'+tree.type)
		return method(tree, flags, verbose)

	def get_code(self):
		return self.code

	def format(self, line = ""):
		''' indent a line according to its level '''
		spaces = 4 * self.level
		return " "*spaces + line

	def level_up(self):
		''' +1 indent; TODO: create new scope '''
		self.level += 1

	def level_down(self):
		''' -1 indent; TODO: remove old scope '''
		self.level -= 1

	def beginning(self):
		imports = "import os, sys\n"
		return imports

	def end(self):
		# extract command line args from main_args
		# and format to int(sys.argv[1]), int(sys.argv[2])
		numOfArgs = len(self.main_args)
		i = 1
		argStr = ""
		while i <= numOfArgs:
			if self.main_types[i-1] == "int":
				argStr += "int(sys.argv[%d]), " % (i)
			elif self.main_types[i-1] == "double":
				argStr += "float(sys.argv[%d]), " % (i)
			else:
				argStr += "sys.argv[%d], " % (i)
			i += 1
		if len(argStr) > 0:
			argStr = argStr[0:-2]
		return "\n\nif __name__ == '__main__':\n\tmain(%s)" % (argStr)

	# --------------------
	# handle grammar nodes
	# --------------------

	# passes testsuite tests 0, 1, 2, 3, 5, 8; works for hello.svel

	# TODO: make sure that we return and are concatenating string types

	def _outer_unit(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: outer_unit"

		return self.walk(tree.children[0], verbose=verbose) + "\n\n" + self.walk(tree.children[1], verbose=verbose)

	def _lang_def(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: lang_def"

		if tree.leaf == "None":
			return ""

		# if lang=Java, copy in java files
		if tree.leaf == "Java":
			jfileutil = open("jfileutil.py").read()
			jfunct = open("jfunct.py").read()
			return jfileutil + "\n\n" + jfunct
		elif tree.leaf == "C":
			cfileutil = open("cfileutil.py").read()
			cfunct = open("cfunct.py").read()
			return cfileutil + "\n\n" + cfunct
		#elif tree.leaf == "Python":
			# implement
		else:
			sys.exit("ERROR: Unrecognized language type.")

	def _translation_unit(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: translation_unit"
		if len(tree.children) == 1:
			return self.walk(tree.children[0], verbose=verbose)
		elif len(tree.children) == 2:
			return self.walk(tree.children[0], verbose=verbose) + "\n\n" + self.walk(tree.children[1], verbose=verbose)

	def _external_declaration(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: external_declaration"

		# if function_def
		if tree.leaf == None:
			return self.walk(tree.children[0], verbose=verbose)

		# if external var declaration
		else:
			return ""
			#return self.walk(tree.children[0]) + " " + tree.leaf

	def _function_def(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: function_def"

		# TODO: use the format function to do indenting
		if len(tree.children) == 2: # main
			line = "def main("
			cl_args = self.walk(tree.children[0], flags=["main"], verbose=verbose)
			line += cl_args
			line += "):\n"

			# parse cl_args to insert into generated code
			cl_args = cl_args.split(",")
			for arg in cl_args:
				if arg != '':
					arg = arg.strip()
					self.main_args.append(arg)

			self.level_up()
			line += self.walk(tree.children[1], verbose=verbose)
			self.level_down()

		elif tree.children[0].leaf == "VOID":
			# TODO: do something with the return type?
			print "returns VOID"
			line = "def "
			line += tree.leaf
			line += "("
			line += self.walk(tree.children[1], verbose=verbose)
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[2], verbose=verbose)
			self.level_down()

		else: # function returning a type
			# TODO: do something with the return type?
			# type is in tree.children[0]
			print "returns" + tree.children[0].leaf
			line = "def "
			line += tree.leaf
			line += "("
			line += self.walk(tree.children[1], verbose=verbose)
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[2], verbose=verbose)
			self.level_down()

		return line

	def _param_list(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: param_list"

		line = ""

		# if there's another parameter
		if len(tree.children) == 2:
			line += self.walk(tree.children[0], flags, verbose=verbose)
			line += ', '
			line += self.walk(tree.children[1], flags, verbose=verbose)

		else: # last parameter in list
			line += self.walk(tree.children[0], flags, verbose=verbose)

		return line

	def _parameter(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: parameter"

		# TODO command line args hack
		if len(flags) == 1 and flags[0] == "main":
			self.main_types.append(tree.children[0].leaf)

		# if empty --> _empty
		if tree.leaf == None:
			return self.walk(tree.children[0], verbose=verbose)

		# TODO: add entry to symbol table
		# type = self.walk(tree.children[0])

		# put ID in code
		return tree.leaf

	def _empty(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: empty"
		return ""

	def _type(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: type"
		return tree.leaf

	def _brack_stmt(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: brack_stmt"
		return self.walk(tree.children[0], verbose=verbose)

	def _stmts(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: stmts"

		line = ""
		if len(tree.children) == 2:
			# consecutive stmts
			line += self.walk(tree.children[0], verbose=verbose)
			line += '\n'
			line += self.walk(tree.children[1], verbose=verbose)

		else:
			# stmt or brack_stmt
			line += self.walk(tree.children[0], verbose=verbose)

		return line

	def _stmt(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: stmt"
		return self.format(self.walk(tree.children[0], verbose=verbose))

	# expressions...
	def _expression_stmt(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: expression_stmt"
		return self.walk(tree.children[0], verbose=verbose)

	def _expression(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: expression"
		return self.walk(tree.children[0], verbose=verbose)

	def _assignment_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: assignment_expr"

		# TODO: handle FUNCT!
		if tree.leaf == None:
			# logical_OR_expression
			return self.walk(tree.children[0], verbose=verbose)

		elif len(tree.children) == 3:
			# FUNCT ID ASSIGN LBRACE funct_name COMMA LPAREN reserved_languages_list RPAREN COMMA primary_expr RBRACE
			return tree.leaf + " = Funct(" + self.walk(tree.children[0], verbose=verbose) + \
				", [" + self.walk(tree.children[1], verbose=verbose) + \
				"], " + self.walk(tree.children[2], verbose=verbose) + ")"

		elif len(tree.children) == 2:
			# initial declaration w/ assignment
			# TODO: do something with the type (symbol table)
			if self.walk(tree.children[0], verbose=verbose) == "file":
				line = "if(not os.path.isfile("
				line += self.walk(tree.children[1], verbose=verbose) + ")):\n"
				
				next_line = "sys.exit('Cannot find "
				self.level_up()
				next_line = self.format(next_line)
				self.level_down()
				next_line += self.walk(tree.children[1], verbose=verbose) + "')\n"

				# this line serves as pseudo-symbol table until we get one
				# TODO: actually use symbol table
				file_name = self.walk(tree.children[1], verbose=verbose)
				janky_line = tree.leaf + "=" + file_name
				janky_line = self.format(janky_line)

				return line + next_line + janky_line + '\n'
			else:
				return tree.leaf + " = " + str(self.walk(tree.children[1], verbose=verbose))

		elif len(tree.children) == 1:
			# assignment
			return tree.leaf + " = " + str(self.walk(tree.children[0], verbose=verbose))


		return self.walk(tree.children[0], verbose=verbose)

	def _logical_OR_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: logical_OR_expr"

		line = ""
		if len(tree.children) == 2:
			# logical_OR_expr OR logical_AND_expr
			line += str(self.walk(tree.children[0], verbose=verbose))
			line += " or "
			line += str(self.walk(tree.children[1], verbose=verbose))

		else:
			# go to logical_AND_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0], verbose=verbose))

		return line

	def _logical_AND_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: logical_AND_expr"

		line = ""
		if len(tree.children) == 2:
			# logical_AND_expr OR equality_expr
			line += str(self.walk(tree.children[0], verbose=verbose))
			line += " and "
			line += str(self.walk(tree.children[1], verbose=verbose))

		else:
			# go to equality_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0], verbose=verbose))

		return line

	def _equality_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: equality_expr"

		line = ""
		if len(tree.children) == 2:
			# equality_expr EQ/NEQ relational_expr
			line += str(self.walk(tree.children[0], verbose=verbose))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1], verbose=verbose))

		else:
			# go to relational_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0], verbose=verbose))

		return line

	def _relational_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: relational_expr"

		line = ""
		if len(tree.children) == 2:
			# relational_expr LS_OP/LE_OP/GR_OP/GE_OP additive_expr
			line += str(self.walk(tree.children[0], verbose=verbose))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1], verbose=verbose))

		else:
			# go to additive_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0], verbose=verbose))

		return line


	def _additive_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: additive_expr"

		line = ""
		if len(tree.children) == 2:
			# additive_expr PLUS/MINUS multiplicative_expr
			line += str(self.walk(tree.children[0], verbose=verbose))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1], verbose=verbose))

		else:
			# go to multiplicative_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0], verbose=verbose))

		return line

	def _multiplicative_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: multiplicative_expr"

		line = ""
		if len(tree.children) == 2:
			# multiplicative_expr TIMES/DIVIDE secondary_expr
			line += str(self.walk(tree.children[0], verbose=verbose))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1], verbose=verbose))

		else:
			# go to multiplicative_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0], verbose=verbose))

		return line

	def _secondary_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: secondary_expr"

		line = ""
		if tree.leaf == None:
			# -> primary_expr
			line += str(self.walk(tree.children[0], verbose=verbose))

		elif tree.leaf == '(':
			# -> LPAREN expression RPAREN
			# -> LPAREN identifier_list RPAREN
			line += '[' + str(self.walk(tree.children[0], verbose=verbose)) + ']'

		elif tree.leaf == '{':
			# -> LBRACE identifier_list RBRACE
			line += '[' + str(self.walk(tree.children[0], verbose=verbose)) + ']'

		return line

	def _primary_expr(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: primary_expr"

		if len(tree.children) == 0:
			# if not function_call or ref_type
			return tree.leaf

		return self.walk(tree.children[0], verbose=verbose)

	def _function_call(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: function_call"

		line = ""
		
		# -> PRINT primary_expr
		if tree.leaf == "print":
			line += tree.leaf + " " + self.walk(tree.children[0], verbose=verbose)
		
		# type conversions hack
		elif tree.leaf == "string":
			line += "str(" + self.walk(tree.children[0], verbose=verbose) + ")"
		elif tree.leaf == "int":
			line += "int(" + self.walk(tree.children[0], verbose=verbose) + ")"
		elif tree.leaf == "double":
			line += "float(" + self.walk(tree.children[0], verbose=verbose) + ")"
		elif tree.leaf == "boolean":
			line += "bool(" + self.walk(tree.children[0], verbose=verbose) + ")"
		
		# lib functions:
		# -> ID PERIOD lib_function LPAREN identifier_list RPAREN
		elif len(tree.children) == 2:
			# TODO: make less hack-y
			function = self.walk(tree.children[0], verbose=verbose)
			if function == "size":
				line += "len(" + tree.leaf + ")"
			elif function == "replace":
				args = self.walk(tree.children[1], verbose=verbose).split(",")
				line += tree.leaf + "[" + args[0].strip() + "] = " + args[1].strip()
			# TODO: make less hack-y when we have a symbol table
			elif function == "readlines":
				line += "[line.strip() for line in open(%s)]" % (tree.leaf)
			else:	
				if function == "remove":
					function = "pop"
					
				line += tree.leaf + "." + function + "(" + self.walk(tree.children[1], verbose=verbose) +")"

		# -> ID LPAREN identifier_list RPAREN
		elif len(tree.children) == 1:
			line += tree.leaf + "(" + self.walk(tree.children[0], verbose=verbose) + ")"

		return line

	def _lib_function(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: function_call"

		if tree.leaf == "assert":
			# -> ASSERT
			return "_assert"
		elif tree.leaf == "readlines":
			# -> READLINE
			# lines = [line.strip() for line in open(input_file)]
			#line = "[line.strip() for line in open("
			#line += self.walk(tree.children[1], verbose=verbose) + ")]"
			return "readlines"
		else:
			# -> REMOVE | SIZE | INSERT | REPLACE
			return tree.leaf # TODO: will need to do type checking somewhere to make sure this is being called on an array/list


	def _ref_type(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: ref_type"

		line = ""
		line += self.walk(tree.children[0], verbose=verbose)
		line += '['
		line += str(self.walk(tree.children[1], verbose=verbose))
		line += ']'
		return line		

	def _reserved_languages_list(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: reserved_languages_list"
		
		line = ""
		if len(tree.children) == 1:
			# -> reserved_languages_keyword
			line += "\"" + self.walk(tree.children[0], verbose=verbose) + "\""

		elif len(tree.children) == 2:
			# -> reserved_languages_list COMMA reserved_languages_keyword
			line += self.walk(tree.children[0], verbose=verbose) + ", \"" + self.walk(tree.children[1], verbose=verbose) + "\""

		return line

	def _reserved_languages_keyword(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: reserved_languages_keyword"
		
		if len(tree.children) == 1 and tree.leaf=="*":
			# -> reserved_languages_keyword TIMES
			return self.walk(tree.children[0]) + " " + tree.leaf
		elif isinstance(tree.leaf, basestring):
			# -> RES_LANG LBRACKET RBRACKET
			# -> RES_LANG
			return tree.leaf
		# -> empty
		return self.walk(tree.leaf)

	def _identifier_list(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: _identifier_list"

		line = ""
		if len(tree.children) == 1:
			# -> expression
			line += str(self.walk(tree.children[0], verbose=verbose))

		elif len(tree.children) == 2 and tree.children[1].leaf=="verbose":
			line += str(self.walk(tree.children[0], verbose=verbose)) + ", verbose=True"

		elif len(tree.children) == 2:
			# -> identifier_list COMMA expression
			line += str(self.walk(tree.children[0], verbose=verbose)) + ", " + str(self.walk(tree.children[1], verbose=verbose))

		return line

	def _ifelse_stmt(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: _ifelse_stmt"

		line = ""
		if len(tree.children) == 2:
			# if
			line += "if "
			line += self.walk(tree.children[0], verbose=verbose)
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1], verbose=verbose)
			self.level_down()

		elif len(tree.children) == 3:
			# if-else
			line += "if "
			line += self.walk(tree.children[0], verbose=verbose)
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1], verbose=verbose) + "\n"
			self.level_down()

			# need to format this line since it's not the beginning of the stmt
			line += self.format("else:\n")

			self.level_up()
			line += self.walk(tree.children[2], verbose=verbose)
			self.level_down()

		return line

	def _loop_stmt(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: _loop_stmt"

		line = ""
		if len(tree.children) == 2:
			# while
			line += "while "
			line += self.walk(tree.children[0], verbose=verbose)
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1], verbose=verbose)
			self.level_down()

		elif len(tree.children) == 4:
			# for TODO: refactor -- very hack-y atm
			line += self.walk(tree.children[0], verbose=verbose) + '\n'
			line += self.format("while ")
			line += self.walk(tree.children[1], verbose=verbose)
			line += ":\n"

			self.level_up()
			# TODO: insert statements inside the for loop
			line += self.walk(tree.children[3], verbose=verbose) + '\n'
			line += self.format(self.walk(tree.children[2], verbose=verbose))
			self.level_down()

		return line

	def _jump_stmt(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: _jump_stmt"

		line = ""
		if tree.leaf == 'break':
			line = tree.leaf

		elif tree.leaf == 'continue':
			line = tree.leaf

		elif tree.leaf == 'return':
			line += "return "
			line += self.walk(tree.children[0], verbose=verbose)

		return line

	def _funct_name(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: _funct_name"

		if tree.leaf == "__main__":
			return "\"main\""

		return self.walk(tree.leaf, verbose=verbose)

	def _STRINGLITERAL(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: _STRINGLITERAL"
		return tree.leaf

	def _ID(self, tree, flags=None, verbose=False):
		if(verbose):
			print "===> svelTraverse: _ID"
		return tree.leaf
