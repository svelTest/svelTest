# =============================================================================
# pfunct.py
# 
# Python Funct class representing the svel funct primitive; contains the 
# assert() method
#
# assert() : creates new Svel Python file with extracted method to test, compiles 
# the file, and runs it to test the given the input and output
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

import os, sys, subprocess

# don't need this anymore...
#from pfileutil import *

# modeled after jfunct.py and cfunct.py
class Funct(object):

    def __init__(self, name, params, file):
    	'''
    		name - name of the function to test
    		params - array of (python) reslang keywords
    		file - relative path to file
    	'''

    	# from jfunct.py and cfunct.py; TODO: DRY...
    	self.name = name   # name of the Python method to test
    	self.params = []   # list of its parameter types
        for p in params:
            self.params += [p.split("_")[1]] # strip type from p_type
        self.file = file   # file where the Python method lives

        self.sig = self.getSignature() # (string) full Python method signature
        self.retype = self.getRetype() # return type

        # TODO: what if we're testing main...
        self.psvelClass = "Svel" + name # name of svel's helper Python class/file

        # Create Svel<name>.py file
        self.psvelHelper = self.createPHelperFile()

        # Compile Svel<name>.py
        print 90 * "="
        print "Compiling %s" % (self.psvelHelper)
        if self.compilePSvelHelper() == -1:
            print "Compilation failed."
            sys.exit(0)

    def _assert(self, inputValues, outputValues, verbose=False):
    	'''
    		Returns true if the actual output matches the expected output
    		inputValues - input values to test
    		outputValues - corresponding output values
    	'''

    	# from jfunct.py and cfunct.py; TODO: DRY...
    	passed = False
        inputstr = ""
        if not isinstance(inputValues, list):
            inputstr += str(inputValues)
        elif len(inputValues) > 1:
            for val in inputValues:
                inputstr += str(val) + ", "
            inputstr = inputstr[0:-2]
        elif len(inputValues) == 1:
            inputstr = str(inputValues)

        # Run the compiled Svel<methodname> program
        process = self.runPSvelHelper(inputValues, outputValues)
        # TODO: file cleanup

        console = process.stdout.read().strip()
        print console

        # Testing print output
        if self.retype == "void":
            if outputValues in console.strip():
                message = "PASS"
                passed = True
            else:
                message = "FAIL"
                message += "\n\t output: %s\n\texpected: %s" % (console, outputValues)

        # Testing a return value
        else:
            if console == "true":
                message = "PASS"
                passed = True
            else:
                message = "FAIL"
                # console == "returned: " + actual
                message += "\n\t%s\n\texpected: %s" % (console, outputValues)

        if verbose == True:
            print "%s(%s)... %s %s" % (self.name, inputstr, 5*"\t", message)
        if passed == True:
            return True
        return False

    def runPSvelHelper(self, inputValues, outputValues):
    	'''
    		Runs Python helper class
    	'''

    	# from jfunct.py and cfunct.py; TODO: DRY...
    	inputstr = ""
        if not isinstance(inputValues, list):
            inputstr += str(inputValues)
        else:
            for val in inputValues:
                inputstr += str(val) + " "
        process = subprocess.Popen('python %s.py %s %s' % (self.psvelClass, inputstr, str(outputValues)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))

        return process

    def compilePSvelHelper(self):
     	'''
		    Compiles the svel Python helper program that calls and checks the method to test. 
		    Program takes in args <actual parameters> <expected output> (ie input and output)
		    (see constructPHelperCode()).
    	'''

    	# from jfunct.py and cfunct.py; TODO: DRY...
    	process = subprocess.Popen("python %s.py" % (self.psvelClass), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))
        err = process.stderr.read()
        if err:
            print 'Error compiling %s.py\n' % (self.psvelClass)
            print err
            return -1

        return process

    def createPHelperFile(self):
    	'''
    		Creates and writes to the svel Python helper file
    	'''

    	# from jfunct.py and cfunct.py; TODO: DRY...
        slash = "/"
        if os.name == "nt":
            slash = "\\"
        absPath = getAbsPath(self.file)
        array = absPath.split(slash)[0:-1]
        absPath = ""
        for dir in array:
            absPath += dir + slash
        absPath += "Svel%s.py" % (self.name)
        svel = open(absPath, "w+")

        jcode = self.constructPHelperCode()
        svel.write(jcode)
        svel.close()

        return absPath

    def constructPHelperCode(self):
		'''

		'''
		# bool, int, long, float, string, tuple, list, dict

		body = ""
		paramsStr = "" # string of variables to pass into the method to test
		imp = "" # import statements

		i = 0;
		for param in self.params:
			# create string assigning variables to the parsed type from the command line
			# _0 = str(args[0]);

			var = "_" + str(i)
			body += "\t%s = %s(argv[%s])\n" % (var, param, i+1)

			paramsStr += var + ", " # paramStr : "_0, _1, ..."
			i += 1

		paramsStr = paramsStr[0:-2]   # strip the ending ", "; becomes "_0, _1"

		# e.g. Add
		className = getClassName(self.file)

		body += "\n"

		if self.retype != "void":
			# _class = Add()
			body += "\t_class = %s()" % (className)
			body += "\n"

			body += "\texpected = %s(argv[%s])\n" % (param, i+1)
			body += "\n"
			
			# actual = _class.add(x, y)
			body += "\tactual = _class.%s(%s)\n" % (self.name, paramsStr)

			body += "\teq = (expected == actual)\n"
			body += "\tif eq:\n\t\tprint \"true\"\n"
			body += "\telse:\n\t\tprint \"returned: \" + str(actual)\n"
			body += "\n\tsys.stdout.flush()\n"

			# import statement - need to import the class
			imp = "from %s import *" % (className)

		else:
			# had to rename main to _main to avoid name collision
			imp = "from %s import %s as _main" % (className, self.name)

			body += "\t%s(%s)\n" % ("_main", paramsStr)



		pcode = '''import sys
%s

def main(argv):
%s

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv)
''' % (imp, body)

		return pcode

    def getSignature(self):
    	'''
    		Gets the method signature to test from the specified file.
    	'''
    	regexp_params = ""
        if os.name == "nt":
            for p in self.params:
                # regexp for parameters - 0 or more spaces, followed by type, 
                # followed by 1 or more spaces, followed by a comma 
                regexp_params += ".*,"
            regexp_params = regexp_params[0 : len(regexp_params)-1] # take off the extra comma

        else:
            for p in self.params:
                # regexp for parameters - 0 or more spaces, followed by type, 
                # followed by 1 or more spaces, followed by a comma 
                regexp_params += ".*,"
            regexp_params = regexp_params[0 : len(regexp_params)-1] # take off the extra comma

        # one or more spaces, followed by method name, followed by 0 or more spaces
        # followed by open paren, followed by RE for params, and finally a close paren
        if os.name == "nt":
            regexp =  "[[:space:]]*def[[:space]]\+%s[[:space:]]*(%s)" % (self.name, regexp_params)
            grep = "grep %s %s" % (regexp, self.file) # grep command
        else:  
            regexp = "[ ]*def[ ]\+%s[ ]*(%s)" % (self.name, regexp_params)
            grep = "grep \'%s\' %s" % (regexp, self.file) # grep command
        output = subprocess.check_output(grep, shell=True)

        return output.strip() # strip leading/trailing whitespace

    # TODO: do we need to implement this for Python?
    def getRetype(self):
    	'''
  			Gets the return type of the method to test.
    	'''
    	# check if the function contains the return keyword?
    	if self.name == "main":
    		return "void"
    	else:
    		return None

def tests():
    _1 = Funct("add", ["p_int", "p_int"], "../test/python_files/Add.py")
    _1_inputs = [[1, 1], [0, 5], [13, 57]]
    _1_outputs = [2, 5, 191]
    
    i = 0
    while i < len(_1_outputs):
        _1._assert(_1_inputs[i], _1_outputs[i], verbose=True)
        i += 1

    _2 = Funct("main", [], "../test/python_files/HelloWorld.py")
    _2._assert([], "Hello World", verbose=True)

# Uncomment if want to run individually; messes up compiled file though
#if __name__ == "__main__":
#    tests()