# import SvelLexer class
from svelLex import SvelLexer

# instantiate and build lexer
svel = SvelLexer()
svel.build()

# provide some data
data = '''
import HelloWorld.java;
void mainSuccess() {
	
}
void onFailure(){
	
}
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