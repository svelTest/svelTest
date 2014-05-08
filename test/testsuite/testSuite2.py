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

	expressions_relational = '''
	lang = None;
	main(){
		print (1<2);

		print (1>2);

		print (1==1);

		print (1!=1);
	}
	'''

	expressions_math = '''
	lang = None;
	main(){
		print (1+1);

		print (1 - 1);

		print (2*2);

		print (2/2);
	}
	'''

	loops_while = '''
	lang = None;
	main(){
		int i = 0;

		while (i<10){
			i = i +1;
		}
		print (i);
	}
	'''

	loops_for = '''
	lang = None;
	main(){
		for (int i =0; i<10; i=i+1){
			print (i);
		}
	}
	'''

	flow = '''
	lang = None;
	main(){
		int i = 1;
		if (i==1){
			print (1);
		} else {
			print (0);
		}
	}
	'''

	array = '''
	lang = None;
	main(){
		int[] a = {1, 2};
		int[] b = {};
	
		b.insert(1);
		a.remove(0);
		a.replace(0,1);
		a.append(3);

		print (b.size());
		print (a);
	}
	'''

	files = '''
	lang = None;
	main(){
		file f = "exampfile.txt";
		int[] i = f.readlines();
	}
	'''

	input_output = '''
	lang = None;
	main(){
		input inp = (1 , 2);
		output out = "hello";
	}
	'''