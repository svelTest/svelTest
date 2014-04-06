'''
Python Funct class representing the svel funct primitive; contains the assert() method

assert() : creates new Svel Java file with extracted
method to test, compiles the file, and runs it to test 
the given the input and output

'''

import os, sys, subprocess
from jcreator import Jcreator
from jfileutil import *

class Funct(object):

    '''
        file - "rel/path/to/file"
        name - name of method to test
        params - array of reslang keywords
    '''
    def __init__(self, name, params, file):
        self.file = file
        self.name = name
        self.params = []
        for p in params:
            self.params += [p.split("_")[1]] # strip type from j_type
        self.cwd = os.getcwd()
        self.sig = self.getSignature()
        self.retype = self.getReType()

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
    def getReType(self):
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

    '''
    Asserts if the actual output matches the expected output, given an input array
        inputs -    test input values
        output -    corresponding test output value
    '''
    def _assert(self, inputs, output):
        jcreator = Jcreator(self.file, self.name, self.params, self.retype)
        jsvelPath = jcreator.createJavaFile()

        # Name of the new Java class -- Svel<methodName>
        jsvel = getClassName(jsvelPath)
        
        print 90 * "="
        # Compile Svel<methodName>.java
        print "Compiling %s..." % (jsvelPath)
        process = subprocess.Popen("javac %s.java" % (jsvel), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))
        err = process.stderr.read()
        if err:
            print 'Error compiling %s.java\n' % (jsvel)
            print err
            return

        # Run the compiled Svel<methodname> program
        print "Running %s...\n" % (jsvelPath)
        inputstr = ""
        for input in inputs:
            inputstr += str(input) + " "
        process = subprocess.Popen('java %s %s %s' % (jsvel, inputstr, str(output)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))

        # TODO: file cleanup

        # Testing System.out.print output
        if self.retype == "void":
            if output in process.stdout.read():
                print "Test passed"
            else:
                print "Test failed"

        # Testing a return value
        else:
            if "true" in process.stdout.read():
                print "Test passed"
            else:
                print "Test failed"

def examples():
    ex_1 = Funct("add", ["j_int", "j_int"], "../test/java_files/Add.java")
    ex_1._assert([1, 1], 2)
    ex_2 = Funct("main", ["j_String[]"], "../test/java_files/HelloWorld.java")
    ex_2._assert([], "Hello World")

if __name__ == "__main__":
    examples()

