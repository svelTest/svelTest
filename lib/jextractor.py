'''
Provides helper functions to get information about a Java file/class

WIP: test() function (gloabl) creates new Svel Java file with extracted
method to test, compiles the file, and runs it to test the given the input and output

'''

import os, sys, subprocess
from jcreator import Jcreator
from jfileutil import *

class Jextractor(object):

    '''
        file - "rel/path/to/file"
        name - name of method to test
        params - array of reslang keywords
    '''
    def __init__(self, file, name, params):
        self.file = file
        self.name = name
        self.params = []
        for p in params:
            self.params += [p.split("_")[1]] # strip type from j_type
        self.cwd = os.getcwd()

    '''
    Gets the method signature to test from the specified file.
    '''
    def getMethodSignature(self):
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
    def getMethodRetType(self):
        sig = self.getMethodSignature()
        sigArray = sig.split(" ")
        i = 0
        while i < len(sigArray):
            if sigArray[i].startswith(self.name):
                break
            i += 1

        # return type will be the word on the left side of the method name
        return sigArray[i - 1]

    def compileSvelJava(self):
        process = subprocess.Popen('javac Svel.java', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd="/Users/emily/Dropbox/projects/svelTest/test/java_files")

def test(file, methodName, params, inputs, output):
    extractor = Jextractor(file, methodName, params)
    params = extractor.params

    # Get return type of add()
    ret = extractor.getMethodRetType()

    # Create the Svel<methodName>.java file
    jcreator = Jcreator(file, methodName, params, ret)
    svelPath = jcreator.createJavaFile()

    # Name of the new Java class -- Svel<methodName>
    svel = getClassName(svelPath)
    
    # Compile Svel<methodName>.java
    print "Compiling %s..." % (svelPath)
    process = subprocess.Popen("javac %s.java" % (svel), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(file))
    err = process.stderr.read()
    if err:
        print 'Error compiling %s.java\n' % (svel)
        print err
        return

    # Run the compiled Svel<methodname> program
    print "Running %s..." % (svelPath)
    inputstr = ""
    for input in inputs:
        inputstr += str(input) + " "
    process = subprocess.Popen('java %s %s %s' % (svel, inputstr, str(output)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd="/Users/emily/Dropbox/projects/svelTest/test/java_files")

    # TODO: file cleanup

    # Testing System.out.print output
    if ret == "void":
        if (output in process.stdout.read()):
            print "Test passed"
        else:
            print "Test failed"

    # Testing a return value
    else:
        if ("true" in process.stdout.read()):
            print "Test passed"
        else:
            print "Test failed"

'''
Tests: 
- extract the add() method in Add.java
- extract the main method in HelloWorld.java
'''
test("../test/java_files/Add.java", "add", ["j_int", "j_int"], [1, 1], 2)
test("../test/java_files/HelloWorld.java", "main", ["j_String[]"], [], "Hello World")

