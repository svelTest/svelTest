# get to lib for svelLex file
import os, sys
lib_path = os.path.join('../lib')
sys.path.append(lib_path)

# get to ply
lib_path = os.path.join('../lib/ply-3.4')
sys.path.append(lib_path)

# import SvelLexer class
from svelLex import SvelLexer

# instantiate and build lexer
svel = SvelLexer()
svel.build()

# provide some data
data = '''
// Testing this type of comment
import HelloWorld.java;

/* Testing this type of comment */
void mainSuccess() {
	
}
void onFailure(){
	
}
/** Testing this type of comment
* Testing
* Testing
*/
main() {
	param noParams = ();
	output systemOut = {SYSOUT, "Hello World"};
	testcase sysoutTestCase = {noParams, systemOut};

	test programTest = {MAIN, sysoutTestCase, mainSuccess, onFailure};
	programTest.test();
}
'''

# print the results of tokenizing
print svel.tok_str(data)