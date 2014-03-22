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