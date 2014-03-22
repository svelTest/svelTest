# get to lib for svelLex file
import os, sys
lib_path = os.path.join('../lib')
sys.path.append(lib_path)

# get to ply
lib_path = os.path.join('../lib/ply-3.4')
sys.path.append(lib_path)

# import lexer class
from svelLex import SvelLexer

# import parser
import svelYacc

# get and build lexer
svel = SvelLexer()
svel.build()

# get parser
parser = svelYacc.getParser()

# provide some data
data = '''
main() {
    testcase sysoutTestCase = {noParams, systemOut};
}
'''

# print the results of parsing
print parser.parse(data, lexer=svel.get_lexer())