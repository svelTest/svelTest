<<<<<<< HEAD
# for exceptions
import sys

=======
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
>>>>>>> 91f2462320b054421642667e828bfd2c3669a5a9
class SvelTraverse(object):

	def __init__(self, tree):

		# scope/indentation level
		self.level = 0

		# keep track of variables in scope
		self.scopes = [[]]

		# symbol table: var --> type
		self.symbols = {}

		# value table: var --> value
		self.values = {}

		# run
		self.code = self.beginning() + self.walk(tree) + self.end()

	# --------------
	# util methods
	# --------------

	def walk(self, tree, flags=None):
		''' call appropriate method based on the node type '''
		if isinstance(tree, list):
			for item in tree:
				walk(item, flags)
			return

		method = getattr(self, '_'+tree.type)
		return method(tree, flags)

	def get_code(self):
		''' return the generated python code'''
		return self.code

	def format(self, line = ""):
		''' indent a line according to its level '''
		spaces = 4 * self.level
		return " "*spaces + line

	def level_up(self):
		''' +1 indent; TODO: create new scope '''
		self.level += 1
		# keep track of variables in scope. for each new variable, add to this list
		# on exit, go through this list and remove from symbols and values
		# variable name should be str(scope) + var_name

		# symbol table: str(scope) + var_name ==> type?
		# value table: str(scope) + var_name ==> value
		#  is this too slow? - every variable access is a string concat

		# add new list of variables for this scope
		self.scopes.append([])

	def level_down(self):
		''' -1 indent; TODO: remove old scope '''
		print self.scopes
		print self.symbols
		print self.values

		# get rid of variables from symbol and value tables
		for var in self.scopes[self.level]:
			del self.symbols[var]

			# replace with stored value
			if (str(self.level) + var) in self.symbols:
				self.symbols[var] = self.symbols[str(self.level) + var]
				del self.symbols[str(self.level) + var]

			if var in self.values:
				del self.values[var]

				# replace
				if(str(self.level) + var) in self.values:
					self.values[var] = self.values[str(self.level) + var]
					del self.values[str(self.level) + var]

		# remove level entry in scopes list
		del self.scopes[self.level]

		# decrement level
		self.level -= 1

	def beginning(self):
		''' static code segments inserted before generated code '''
		return "import os, sys\n\n"

	def end(self):
		''' static code segments inserted after generated code '''
		return "\n\nif __name__ == '__main__':\n    main()"

	# --------------------
	# handle grammar nodes
	# --------------------

	# passes testsuite tests 0, 1, 2, 3, 5, 8; works for hello.svel
	# TODO: make sure that we return and are concatenating string types; assert?

	def _translation_unit(self, tree, flags=None):
		print "===> svelTraverse: translation_unit"
		if len(tree.children) == 1:
			# -> external_declaration
			return self.walk(tree.children[0])

		elif len(tree.children) == 2:
			# -> translation_unit external_declaration
			return self.walk(tree.children[0]) + "\n\n" + self.walk(tree.children[1])

	def _external_declaration(self, tree, flags=None):
		print "===> svelTraverse: external_declaration"

		if tree.leaf == None:
			# -> function_def
			return self.walk(tree.children[0])

		else:
			# TODO: handle the global var declaration
			return ""
			#return self.walk(tree.children[0]) + " " + tree.leaf

	def _function_def(self, tree, flags=None):
		print "===> svelTraverse: function_def"

		if len(tree.children) == 2:
			# -> MAIN LPAREN param_list RPAREN brack_stmt
			line = "def main("
			line += self.walk(tree.children[0])
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[1])

			self.level_down()

		elif tree.children[0].leaf == "VOID":
			# -> VOID ID LPAREN param_list RPAREN brack_stmt
			line = "def "
			line += tree.leaf
			line += "("
			line += self.walk(tree.children[1])
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[2])
			self.level_down()

		else:
			# -> type ID LPAREN param_list RPAREN brack_stmt
			# TODO: do something with the return type?
			# type is in tree.children[0]
			line = "def "
			line += tree.leaf
			line += "("
			line += self.walk(tree.children[1])
			line += "):\n"

			self.level_up()
			line += self.walk(tree.children[2])
			self.level_down()

		return line

	def _param_list(self, tree, flags=None):
		print "===> svelTraverse: param_list"

		line = ""
		if len(tree.children) == 2:
			# -> param_list COMMA param
			line += self.walk(tree.children[0])
			line += ', '
			line += self.walk(tree.children[1])

		else:
			# -> param
			line += self.walk(tree.children[0])

		return line

	def _parameter(self, tree, flags=None):
		print "===> svelTraverse: parameter"

		if tree.leaf == None:
			# -> empty
			return self.walk(tree.children[0])

		# TODO: add entry to symbol table
		# type = self.walk(tree.children[0])

		# -> type ID
		return tree.leaf

	def _empty(self, tree, flags=None):
		print "===> svelTraverse: empty"
		return ""

	def _type(self, tree, flags=None):
		print "===> svelTraverse: type"

		# TODO: differentiate the array type
		return tree.leaf

	def _brack_stmt(self, tree, flags=None):
		print "===> svelTraverse: brack_stmt"

		# -> LBRACE stmts RBRACE
		return self.walk(tree.children[0])

	def _stmts(self, tree, flags=None):
		print "===> svelTraverse: stmts"

		line = ""
		if len(tree.children) == 2:
			# -> stmts stmt
			line += self.walk(tree.children[0])
			line += '\n'
			line += self.walk(tree.children[1])

		else:
			# -> stmt
			# -> brack_stmt
			line += self.walk(tree.children[0])

		return line

	def _stmt(self, tree, flags=None):
		print "===> svelTraverse: stmt"
		return self.format(self.walk(tree.children[0]))

	def _expression_stmt(self, tree, flags=None):
		print "===> svelTraverse: expression_stmt"
		return self.walk(tree.children[0])

	def _expression(self, tree, flags=None):
		print "===> svelTraverse: expression"
		return self.walk(tree.children[0])

	def _assignment_expr(self, tree, flags=None):
		print "===> svelTraverse: assignment_expr"

		# TODO: handle FUNCT!
		if tree.leaf == None:
			# -> logical_OR_expression
			return self.walk(tree.children[0])

		else:

			variable_name = tree.leaf

			# keep track of this variable's scope
			self.scopes[self.level].append(tree.leaf)

			if len(tree.children) == 2:
				# -> type ID ASSIGN assignment_expr
				variable_type = str(self.walk(tree.children[0]))
				variable_value = str(self.walk(tree.children[1]))

				# add variable to symbol and value table
				self.assignment_helper(variable_name, variable_value, variable_type)

				return variable_name + " = " + variable_value

			elif len(tree.children) == 1:
				# -> ID ASSIGN assignment_expr
				variable_value = str(self.walk(tree.children[0]))

				# add variable to symbol and value table
				self.assignment_helper(variable_name, variable_value)

				return variable_name + " = " + variable_value

		return self.walk(tree.children[0])

	def assignment_helper(self, var, var_value=None, var_type=None):
		# no type means --> case 2
		# no value means --> case 0
		# both means --> case 1

		# case 0: declaration of new variable (just type, no value)
			# int x;
		# case 1: declaration of new variable and assignment of value (DEFAULT VAL?)
			# int x = 0; (x doesn't exist yet)
			# int x = 0; (x already exists --> new scope or throw error)
		# case 2: assignment of value to existing variable (value may or may not have existed)
			# x = 0; (x in symbol table)
			# x = 0; (x not in symbol table --> throw error)

		# TODO: rethink scoping

		# inner var w/ same name as var in outer scope
		if var_type and var in self.symbols:
			raise Exception("Variable '" + var + "' is already defined in this scope.")

			''' TODO: move this
			self.symbols[str(self.level) + var] = self.symbols[var]
			self.symbols[var] = var_type
			
			# update value table
			if var_value and var in self.values:
				self.values[str(self.level) + var] = self.values[var]
				self.values[var] = var_value
			elif var_value:
				self.values[var] = var_value
			'''
		
		# new var declaration
		elif var_type:
			self.symbols[var] = var_type

			if var_value:
				self.values[var] = var_value

		# assign value to existing var
		else:
			if var in self.symbols:
				self.symbols[str(self.level) + var] = self.symbols[var]

				if var in self.values:
					self.values[var] = var_value
			else:
				raise Exception("Declare variable '" + var + "' before use.")

				
	def _logical_OR_expr(self, tree, flags=None):
		print "===> svelTraverse: logical_OR_expr"

		line = ""
		if len(tree.children) == 2:
			# -> logical_OR_expr OR logical_AND_expr
			line += str(self.walk(tree.children[0]))
			line += " or "
			line += str(self.walk(tree.children[1]))

		else:
			# -> logical_AND_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _logical_AND_expr(self, tree, flags=None):
		print "===> svelTraverse: logical_AND_expr"

		line = ""
		if len(tree.children) == 2:
			# -> logical_AND_expr OR equality_expr
			line += str(self.walk(tree.children[0]))
			line += " and "
			line += str(self.walk(tree.children[1]))

		else:
			# -> equality_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _equality_expr(self, tree, flags=None):
		print "===> svelTraverse: equality_expr"

		line = ""
		if len(tree.children) == 2:
			# -> equality_expr EQ/NEQ relational_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# -> relational_expr
			assert(len(tree.children) == 1) # TODO: is this necessary?

			line += str(self.walk(tree.children[0]))

		return line

	def _relational_expr(self, tree, flags=None):
		print "===> svelTraverse: relational_expr"

		line = ""
		if len(tree.children) == 2:
			# -> relational_expr LS_OP/LE_OP/GR_OP/GE_OP additive_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# -> additive_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line


	def _additive_expr(self, tree, flags=None):
		print "===> svelTraverse: additive_expr"

		line = ""
		if len(tree.children) == 2:
			# -> additive_expr PLUS/MINUS multiplicative_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# -> multiplicative_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _multiplicative_expr(self, tree, flags=None):
		print "===> svelTraverse: multiplicative_expr"

		line = ""
		if len(tree.children) == 2:
			# -> multiplicative_expr TIMES/DIVIDE secondary_expr
			line += str(self.walk(tree.children[0]))
			line += " " + tree.leaf + " "
			line += str(self.walk(tree.children[1]))

		else:
			# -> multiplicative_expr
			assert(len(tree.children) == 1)

			line += str(self.walk(tree.children[0]))

		return line

	def _secondary_expr(self, tree, flags=None):
		print "===> svelTraverse: secondary_expr"

		line = ""
		if tree.leaf == None:
			# -> primary_expr
			line += str(self.walk(tree.children[0]))

		elif tree.leaf == '(':
			# -> LPAREN expression RPAREN
			line += '(' + str(self.walk(tree.children[0])) + ')'

		elif tree.leaf == '{':
			# -> LBRACE identifier_list RBRACE
			line += '[' + str(self.walk(tree.children[0])) + ']'

		return line

	def _primary_expr(self, tree, flags=None):
		print "===> svelTraverse: primary_expr"

		if len(tree.children) == 0:
			# if not function_call
			return tree.leaf

		# -> function_call
		return self.walk(tree.children[0])

	def _function_call(self, tree, flags=None):
		print "===> svelTraverse: function_call"

		# TODO: finish this;

		line = ""
		if tree.leaf == "print":
			line += tree.leaf + " " + tree.children[0].leaf

		return line

	# TODO: implement
	def _reslang_type(self, tree, flags=None):
		print "===> svelTraverse: reslang_type"
		return self.walk(tree.children[0])

	# TODO: implement
	def _reserved_languages_list(self, tree, flags=None):
		print "===> svelTraverse: reserved_languages_list"
		return self.walk(tree.children[0])

	# TODO: implement
	def _reserved_languages_keyword(self, tree, flags=None):
		print "===> svelTraverse: _reserved_languages_keyword"
		return self.walk(tree.children[0])

	def _identifier_list(self, tree, flags=None):
		print "===> svelTraverse: _identifier_list"

		line = ""
		if len(tree.children) == 1:
			# -> expression
			line += str(self.walk(tree.children[0]))

		elif len(tree.children) == 2:
			# -> identifier_list COMMA expression
			line += str(self.walk(tree.children[0])) + ', ' + str(self.walk(tree.children[1]))

		return line

	def _ifelse_stmt(self, tree, flags=None):
		print "===> svelTraverse: _ifelse_stmt"

		line = ""
		if len(tree.children) == 2:
			# -> IF LPAREN expression RPAREN brack_stmt
			line += "if "
			line += self.walk(tree.children[0])
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1])
			self.level_down()

		elif len(tree.children) == 3:
			# -> IF LPAREN expression RPAREN brack_stmt ELSE brack_stmt
			line += "if "
			line += self.walk(tree.children[0])
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1]) + "\n"
			self.level_down()

			# need to format this line since it's not the beginning of the stmt
			line += self.format("else:\n")

			self.level_up()
			line += self.walk(tree.children[2])
			self.level_down()

		return line

	def _loop_stmt(self, tree, flags=None):
		print "===> svelTraverse: _loop_stmt"

		line = ""
		if len(tree.children) == 2:
			# -> (while loop)
			line += "while "
			line += self.walk(tree.children[0])
			line += ":\n"

			self.level_up()
			line += self.walk(tree.children[1])
			self.level_down()

		elif len(tree.children) == 4:
			# -> (for loop)
			# TODO: refactor -- very hack-y atm
			line += self.walk(tree.children[0]) + '\n'
			line += self.format("while ")
			line += self.walk(tree.children[1])
			line += ":\n"

			self.level_up()
			# TODO: insert statements inside the for loop
			line += self.walk(tree.children[3]) + '\n'
			line += self.format(self.walk(tree.children[2]))
			self.level_down()

		return line

	def _jump_stmt(self, tree, flags=None):
		print "===> svelTraverse: _jump_stmt"

		line = ""
		if tree.leaf == 'break':
			# -> break
			line = tree.leaf

		elif tree.leaf == 'continue':
			# -> continue
			line = tree.leaf

		elif tree.leaf == 'return':
			#-> return
			line += "return "
			line += self.walk(tree.children[0])

		return line

	# TODO: double-check implementation
	def _funct_name(self, tree, flags=None):
		print "===> svelTraverse: _funct_name"
		return tree.leaf