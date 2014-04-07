'''
Python Funct class representing the svel funct primitive; contains the assert() method

assert() : creates new Svel Java file with extracted
method to test, compiles the file, and runs it to test 
the given the input and output

'''

import os, sys, subprocess
from jfileutil import *

class Funct(object):

    '''
        file - "rel/path/to/file"
        name - name of method to test
        params - array of reslang keywords
    '''
    def __init__(self, name, params, file):
        self.name = name   # name of the Java method to test
        self.file = file   # file where the Java method lives
        self.params = []   # list of its parameter types
        for p in params:
            self.params += [p.split("_")[1]] # strip type from j_type

        self.sig = self.getSignature() # (string) full Java method signature
        self.retype = self.getRetype() # return type

        self.jsvelClass = "Svel" + name
        self.jsvelHelper = self.createJHelperFile()

        print 90 * "="
        # Compile Svel<methodName>.java
        print "Compiling %s" % (self.jsvelHelper)
        if self.compileJSvelHelper() == -1:
            print "Compilation failed."
            return

    '''
    Asserts if the actual output matches the expected output, given an input array
        inputs -    test input values
        output -    corresponding test output value
    '''
    def _assert(self, inputValues, outputValue):

        inputstr = ""
        if len(inputValues) > 1:
            for val in inputValues:
                inputstr += str(val) + ", "
            inputstr = inputstr[0:-2]
        elif len(inputValues) == 1:
            inputstr = str(inputValues)

        # Run the compiled Svel<methodname> program
        process = self.runJSvelHelper(inputValues, outputValue)
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


        print "%s(%s)... %s %s" % (self.name, inputstr, 5*"\t", message)
        if message == "PASSED":
            return True
        return False

    def runJSvelHelper(self, inputValues, outputValue):
        inputstr = ""
        for val in inputValues:
            inputstr += str(val) + " "
        process = subprocess.Popen('java %s %s %s' % (self.jsvelClass, inputstr, str(outputValue)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))

        return process

    '''
    Compiles the svel Java helper program that calls and checks the method to test. 
    Program takes in args <actual parameters> <expected output> (ie input and output)
    (see constructJHelperCode()).
    '''
    def compileJSvelHelper(self):
        process = subprocess.Popen("javac %s.java" % (self.jsvelClass), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=getAbsDir(self.file))
        err = process.stderr.read()
        if err:
            print 'Error compiling %s.java\n' % (self.jsvelClass)
            print err
            return -1

        return process

    '''
    Creates and writes to the svel Java helper file
    '''
    def createJHelperFile(self):
        absPath = getAbsPath(self.file)
        array = absPath.split("/")[0:-1]
        absPath = ""
        for dir in array:
            absPath += dir + "/"
        absPath += "Svel%s.java" % (self.name)
        svel = open(absPath, "w")

        jcode = self.constructJHelperCode()
        svel.write(jcode)
        svel.close()

        return absPath

    '''
    Constructs the Java source code for the svel Java helper file, which
    calls and checks the method to test
    
    For example, Sveladd.java looks something like this
    public class Svel {
        public static void main(String[] args) {
            int _0 = Integer.parseInt(args[0]); // reads args passed svel's Java program
            int _1 = Integer.parseInt(args[1]);
            int expected = Integer.parseInt(args[2]);

            int actual = Add.add(_0, _1);

            System.out.println(expected == actual);
        }
    }

    To run the program :
    $ java Svel 1 1 2
    '''
    def constructJHelperCode(self):
        jtypes = {
            "int"       : "Integer",
            "double"    : "Double",
            "float"     : "Float",
            "char"      : "Character",
            "byte"      : "Byte",
            "long"      : "Long",
            "String"    : "String"
        }

        body = ""
        paramsStr = "" # string of variables to pass into the method to test

        i = 0;
        for param in self.params:
            # create string assigning variables to the parsed type from the command line
            # int _0 = Integer.parseInt(args[0]);
            paramCap = param.capitalize()
            var = "_" + str(i)
            if not param.startswith("String"):
                body += "\t\t%s %s = %s.parse%s(args[%d]);\n" % (param, var, jtypes[param], paramCap, i)
            else:
                body += "\t\t%s %s = args;\n" % (param, var)
            
            paramsStr += var + ", " # paramStr : "_0, _1, ..."
            i += 1

        paramsStr = paramsStr[0:-2]   # strip the ending ", "; becomes "_0, _1"

        body += "\n"

        if self.retype != "void":
            retypeCap  = self.retype.capitalize()
            body += "\t\t%s expected = %s.parse%s(args[%d]);\n" % (self.retype, jtypes[self.retype], retypeCap, i)
            body += "\n"
            body += "\t\t%s actual = %s.%s(%s);\n" % (self.retype, getClassName(self.file), self.name, paramsStr)
            body += "\t\tSystem.out.println(expected == actual);"

        else:
            body += "\t\t%s.%s(%s);\n" % (getClassName(self.file), self.name, paramsStr)

        jcode = '''
public class Svel%s {
    public static void main(String[] args) 
    {
%s
    }
}''' % (self.name, body)

        return jcode

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


def tests():
    _1 = Funct("add", ["j_int", "j_int"], "../test/java_files/Add.java")
    _1_inputs = [[1, 1], [0, 5], [13, 57]]
    _1_outputs = [2, 5, 191]
    
    i = 0
    while i < len(_1_outputs):
        _1._assert(_1_inputs[i], _1_outputs[i])
        i += 1

    _2 = Funct("main", ["j_String[]"], "../test/java_files/HelloWorld.java")
    _2._assert([], "Hello World")

if __name__ == "__main__":
    tests()

