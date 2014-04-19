class Testsuite(object):

	def __init__(self):

		# 0: print Hello World
		test_0 = '''
		main() {
			print "Hello world";
		}
		'''

		# 1: equality, additive, multiplicative, and relational expressions
		test_1 = '''
		main() {
			int x = 1;
			int y = 2;
			int z = x + y;

			int a = x * y;

			boolean b = x < y;
		}
		'''

		# 2: function def with empty parameter list and void return type
		test_2 = '''
		void foo() {
			string f = "foo";
		}
		'''	

		# 3: function definition with parameters and return type
		test_3 = '''
		int add(int x, int y) {
			int z = x + y;
		}
		'''	

		# 4: function definition with parameters and return type
		test_4 = '''
		int add(int x, int y) {
			int[] z = {x, y};
		}
		'''	

		# 5: while loop, double, assignment expression without type
		test_5 = '''
		main() {
			double i = 0.0;
			while(i < 10) {
				i = i + 1;
			}
		}
		'''	
		# 6: call assert() with inline input/output 
		test_6 = '''
		main() {
			file helloFile = "java_files/Hello.java";
			funct helloMain = {__main__, (j_String[]), helloFile};
			helloMain.assert((), "Hello World!");
		}
		'''

		# 7: full Hello World test
		test_7 = '''
		void helloWorldTest() {
			file helloFile = "../Hello.java";
			funct helloMain = {__main__, (), helloFile};
			input in = ();
			output out = "Hello World!";
			helloMain.assert(in, out);
		}
		'''

		# 8: for loop
		test_8 = '''
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
		void arrays(int x, int y, int z) {
			int[] a = {x, y, z};
			int b = a[1];
		}
		'''

		# 11: more adv array initialization and access
		test_11 = '''
		void createInputArray() {
			input[] in = {0, 1, 2};
			output[] out = {0, 1, 2};
			for (int i = 0; i < 3; i=i+1) {
				if (in[i] != out[i]) {
					break;
				}
			}
		}
		'''

		# 12: declare input type with ()
		test_12 = '''
		boolean testAdd() {
			file addFile = "java_files/Add.java";
			funct addFunct = {"add", (j_int, j_int), addFile};
			input in = (3, 4);
			output out = 7;
			return addFunct.assert(in, out);
		}
		'''

		self.cases = [test_0, test_1, test_2, test_3, test_4, test_5, test_6, test_7, test_8, test_9, test_10, test_11, test_12]

	def get(self, i):
		return self.cases[i]

	def getAll(self):
		return self.cases