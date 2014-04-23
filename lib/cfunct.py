# =============================================================================
# cfunct.py
# 
# Python Funct class representing the svel funct primitive; contains the 
# assert() method
#
# assert() : creates new Svel C file with extracted method to test, compiles 
# the file, and runs it to test the given the input and output
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

import os, sys, subprocess
# don't need this line anymore because cfileutil already present in compiled file
#from cfileutil import *

class Funct(object):

    '''
        file - "rel/path/to/file"
        name - name of method to test
        params - array of reslang keywords
    '''
    def __init__(self, name, params, file):
        self.name = name   # name of the C method to test
        self.file = file   # file where the C method lives
        self.params = []   # list of its parameter types
        for p in params:
            self.params += [p.split("_")[1]] # strip type from c_type

        self.sig = self.getSignature() # (string) full C method signature
        self.retype = self.getRetype() # return type
        self.csvelClass = "Svel" + name # name of svel's helper C class/file

        # Create Svel<name>.c file
        self.csvelHelper = self.createCHelperFile()

        # Compile Svel<name>.c
        print 90 * "="
        print "Compiling %s" % (self.csvelHelper)
        if self.compileCSvelHelper() == -1:
            print "Compilation failed."
            return

    '''
    Asserts if the actual output matches the expected output, given an input array
        inputs -    test input values
        output -    corresponding test output value
    '''
    def _assert(self, inputValues, outputValue, verbose=False):

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
        process = self.runCSvelHelper(inputValues, outputValue)
        # TODO: file cleanup

        # Testing System.out.print output
        if self.retype == "void":
            if outputValue in process.stdout.read():
                message = "PASS"
            else:
                message = "FAIL"

        # Testing a return value
        else:
            if "true" in process.stdout.read():
                message = "PASS"
            else:
                message = "FAIL"


        if verbose == True:
            print "%s(%s)... %s %s" % (self.name, inputstr, 5*"\t", message)
        if message == "PASS":
            return True
        return False

    def runCSvelHelper(self, inputValues, outputValue):
        inputstr = ""
        if not isinstance(inputValues, list):
            inputstr += str(inputValues)
        else:
            for val in inputValues:
                inputstr += str(val) + " "
        process = subprocess.Popen('./%s %s %s' % (self.csvelClass, inputstr, str(outputValue)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))

        return process

    '''
    Compiles the svel C helper program that calls and checks the method to test. 
    Program takes in args <actual parameters> <expected output> (ie input and output)
    (see constructCHelperCode()).
    '''
    def compileCSvelHelper(self):
        process = subprocess.Popen("gcc -o %s" % (self.csvelClass), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))
        err = process.stderr.read()
        if err:
            print 'Error compiling %s.c\n' % (self.csvelClass)
            print err
            return -1

        return process

    '''
    Creates and writes to the svel C helper file
    '''
    def createCHelperFile(self):
        absPath = getAbsPath(self.file)
        array = absPath.split("/")[0:-1]
        absPath = ""
        for dir in array:
            absPath += dir + "/"
        absPath += "Svel%s.c" % (self.name)
        svel = open(absPath, "w")

        ccode = self.constructCHelperCode()
        svel.write(ccode)
        svel.close()

        return absPath

    '''
    Constructs the C source code for the svel C helper file, which
    calls and checks the method to test
    
    For example, Sveladd.c looks something like this
    #include <stdio.h>
    #include <stdlib.h>
    int main(int argc, char *argv[]) {
        int _0 = atoi(argv[1]);
        int _1 = atoi(argv[2]);
        int expected = atoi(argv[3]);

        int actual = add(_0, _1);

        // prints 1 if true, 0 if false
        printf("%d\n", expected == actual);
    }

    To run the program :
    $ ./Sveladd 1 1 2
    '''
    def constructCHelperCode(self):
        body = ""
        paramsStr = "" # string of variables to pass into the method to test

        i = 0;
        for param in self.params:
            # create string assigning variables to the parsed type from the command line
            # int _0 = Integer.parseInt(args[0]);
            paramCap = param.capitalize()
            var = "_" + str(i)
            if not param.startswith("char"):
                body += "\t\t%s %s = atoi(argv[%d]);\n" % (param, var, i)
            else:
                body += "\t\t%s %s = argv[%d];\n" % (param, var, i)
            
            paramsStr += var + ", " # paramStr : "_0, _1, ..."
            i += 1

        paramsStr = paramsStr[0:-2]   # strip the ending ", "; becomes "_0, _1"

        body += "\n"

        if self.retype != "void":
            body += "\t\t%s expected = atoi(argv[%d]);\n" % (self.retype, i)
            body += "\n"
            body += "\t\t%s actual = %s.%s(%s);\n" % (self.retype, getClassName(self.file), self.name, paramsStr)
            body += "\t\tprintf(\"%d\\n\", expected == actual);"

        else:
            body += "\t\t%s.%s(%s);\n" % (getClassName(self.file), self.name, paramsStr)

        ccode = '''
#include <stdio.h>
main(int argc, char *argv[]) {
%s
}''' % (body)

        return ccode

    '''
    Gets the method signature to test from the specified file.
    '''
    def getSignature(self):
        regexp_params = ""
        for p in self.params:
            # regexp for parameters - 0 or more spaces, followed by type, 
            # followed by 1 or more spaces, followed by a comma 
            regexp_params += "[ ]*%s[ ]\+.*," % (p)
        regexp_params = regexp_params[0 : len(regexp_params)-1] # take off the extra comma

        # one or more spaces, followed by method name, followed by 0 or more spaces
        # followed by open paren, followed by RE for params, and finally a close paren
        regexp = "[ ]\+%s[ ]*(%s)" % (self.name, regexp_params)
        grep = "grep \'%s\' %s" % (regexp, self.file) # grep command
        output = subprocess.check_output(grep, shell=True)

        return output.strip() # strip leading/trailing whitespace

    '''
    Gets the return type of the method to test.
    '''
    def getRetype(self):
        if (self.sig):
            sig = self.sig
        else:
            sig = self.getSignature()
        sigArray = sig.split(" ")
        i = 0
        while i < len(sigArray):
            if sigArray[i].startswith(self.name):
                break
            i += 1

        # return type will be the word on the left side of the method name
        return sigArray[i - 1]

    def getFunctionDefinition(self):
        regexp_params = ""
        for p in self.params:
            # regexp for parameters - 0 or more spaces, followed by type, 
            # followed by 1 or more spaces, followed by a comma 
            regexp_params += "[ ]*%s[ ]\+.*," % (p)
        regexp_params = regexp_params[0 : len(regexp_params)-1] # take off the extra comma

        # one or more spaces, followed by method name, followed by 0 or more spaces
        # followed by open paren, followed by RE for params, and finally a close paren
        regexp = "[ ]\+%s[ ]*(%s)[ ]*{.*}" % (self.name, regexp_params)
        grep = "grep \'%s\' %s" % (regexp, self.file) # grep command
        output = subprocess.check_output(grep, shell=True)

        return output.strip() # strip leading/trailing whitespace

#def tests():
#    _1 = Funct("add", ["j_int", "j_int"], "../test/java_files/Add.java")
#    _1_inputs = [[1, 1], [0, 5], [13, 57]]
#    _1_outputs = [2, 5, 191]
#    
#    i = 0
#    while i < len(_1_outputs):
#        _1._assert(_1_inputs[i], _1_outputs[i])
#        i += 1
#
#    _2 = Funct("main", ["j_String[]"], "../test/java_files/HelloWorld.java")
#    _2._assert([], "Hello World")

# Uncomment if want to run individually; messes up compiled file though
#if __name__ == "__main__":
#    tests()
