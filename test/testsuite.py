# =============================================================================
# testsuite.py
# 
# Small test cases to run on parser through testParser.py
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

class Testsuite(object):

	def __init__(self):

		# 0: print Hello World
		test_0 = '''
		lang=None;
		main() {
			print("Hello world");
		}
		'''

		# 1: equality, additive, multiplicative, and relational expressions
		test_1 = '''
		int k = 0;
		main() {
			int x = 1;
			int y = 2;
			int z = x + y;

			int a = x * y;

			boolean b = x < y;
			print(x+y);
		}
		'''

		# 2: function def with empty parameter list and void return type
		test_2 = '''
		lang=None;
		void foo() {
			string f = "foo";
		}
		'''	

		# 3: function definition with parameters and return type
		test_3 = '''
		lang=None;
		int add(int x, int y) {
			int z = x + y;
		}
		'''	

		# 4: function definition with parameters and return type
		test_4 = '''
		lang=None;
		int add(int x, int y) {
			int[] z = {x, y};
		}
		'''	

		# 5: while loop, double, assignment expression without type
		test_5 = '''
		lang=None;
		main() {
			double i = 0.0;
			while(i < 10) {
				i = i + 1;
			}
		}
		'''	
		# 6: call assert() with inline input/output 
		test_6 = '''
		lang=Java;
		main() {
			file helloFile = "java_files/Hello.java";
			funct helloMain = {__main__, (j_String[]), helloFile};
			helloMain.assert((), "Hello World!");
		}
		'''

		# 7: full Hello World test
		test_7 = '''
		lang=Java;
		void helloWorldTest() {
			file helloFile = "../Hello.java";
			funct helloMain = {__main__, (), helloFile};
			input _in = ();
			output out = "Hello World!";
			helloMain.assert(_in, out);
		}
		'''

		# 8: for loop
		test_8 = '''
		lang=None;
		int increment(int x) {
			int result = 0;
			for (int i = 0; i < x; i=i+1) {
				result = result + i;
			}
			return result;
		}
		'''

		# 9: for loop with postfix expression -- this should throw a syntax error!
		test_9 = '''
		lang=None;
		int increment(int x) {
			int result = 0;
			for (int i = 0; i < x; i++) {
				result = result + i;
			}
			return result;
		}
		'''

		# 10: simple array initialization and access
		test_10 = '''
		lang=None;
		void arrays(int x, int y, int z) {
			int[] a = {x, y, z};
			int b = a[1];
		}
		'''

		# 11: more adv array initialization and access
		test_11 = '''
		lang=None;
		void createInputArray() {
			input[] _in = {0, 1, 2};
			output[] out = {0, 1, 2};
			for (int i = 0; i < 3; i=i+1) {
				if (_in[i] != out[i]) {
					break;
				}
			}
		}
		'''

		# 12: declare input type with ()
		test_12 = '''
		lang=Java;
		boolean testAdd() {
			file addFile = "java_files/Add.java";
			funct addFunct = {"add", (j_int, j_int), addFile};
			input _in = (3, 4);
			output out = (7);
			return addFunct.assert(_in, out);
		}
		'''

		# 13: list methods -- make sure test_12 still works
		test_13 = '''
		lang=None;
		main() {

			// from LRM
			int[] c = {1, 2, 3};
			c.remove(2); // returns 3, list is now {1, 2}

			int[] d = {1, 2, 3};
			d.size(); // 3

			int[] e = {1, 2, 3};
			e.insert(0, 4); // {4, 1, 2, 3}

			int[] f = {1, 2, 3};
			f.replace(0, 4); // {4, 2, 3}

		}
		'''

		self.cases = [test_0, test_1, test_2, test_3, test_4, test_5, test_6, test_7, test_8, test_9, test_10, test_11, test_12, test_13]

	def get(self, i):
		return self.cases[i]

	def getAll(self):
		return self.cases

from jfunct import Funct
class FunctTests(object):

	def __init__(self):

		# 0: Add.java
		def test_0():
			addFunct = Funct("add", ["j_int", "j_int"], "../test/java_files/Add.java")
			addInputs = [[1, 1], [0, 5], [13, 57]]
			addOutputs = [2, 5, 191]
			
			i = 0
			while i < len(addOutputs):
			    addFunct._assert(addInputs[i], addOutputs[i])
			    i += 1

		# 1: HelloWorld.java
		def test_1():
			helloFunct = Funct("main", ["j_String[]"], "../test/java_files/HelloWorld.java")
			helloFunct._assert([], "Hello World")

		# 2: Fibonacci.java
		def test_2():
			fibFunct = Funct("fib", ["j_int"], "../test/java_files/Fibonacci.java")
			fibInputs = [0, 1, 4, 8]
			fibOutputs = [0, 1, 3, 21]
			i = 0
			while i < len(fibInputs):
			    fibFunct._assert(fibInputs[i], fibOutputs[i])
			    i += 1

		self.cases = [test_0, test_1, test_2]

	def test(self, i):
		self.cases[i]()
		return

	def testAll(self):
		for case in self.cases:
			case()
