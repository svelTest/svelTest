class Testsuite(object):

	# 0: print Hello World
	hello_world = '''
	lang=None;
	main() {
		print("Hello world");
	}
	'''

	comments = '''
	lang=None;
	main(){
		//this is a comment
		print("Hello world");
	}
	'''

	empty = '''
	lang=None;
	main(){
		;
	}
	'''

	assignments = '''
	lang=None;
	main(){
		int a;
		a = 1;
		print (a);

		string b = "hello";
		print (b);
	
	}
	'''

	expressions_boolean = '''
	lang=None;
	main(){
		boolean a = true;
		boolean b = false;

		print(a && b);
		print(a || b);

	}
	'''

