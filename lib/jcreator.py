'''
This class creates the Java source file (Svel.java) that calls and checks the Java method to test.
Each testcase "input" and "output" will be passed into the Java program as command line inputs.
The first command line args will be the inputs, and the last will be the output
That way, this file can be compiled and run with each testcase.

For example, if we're testing add() in Add.java:
1. We create the file Svel.java that looks something like this
public class Svel {
    public static void main(String[] args) {
        int _0 = Integer.parseInt(args[0]);
        int _1 = Integer.parseInt(args[1]);
        int expected = Integer.parseInt(args[2]);

        int actual = Add.add(_0, _1);

        System.out.println(expected == actual);
    }
}

2. Now we can run
    $ javac Svel.java
    $ java Svel 1 1 2

'''
#from jextractor import *
import os

from jfileutil import *

class Jcreator(object):

    '''
        classFilePath   - path to Java class file
        methodName      - name of method to test in the Java class file
        parameterTypes  - array of parameter types for the method to test
        returnType      - return type of method to test
    '''
    def __init__(self, classFilePath, methodName, parameterTypes, returnType):
        self.classFilePath = classFilePath
        self.methodName = methodName
        objNames = {
            "int"       : "Integer",
            "double"    : "Double",
            "float"     : "Float",
            "char"      : "Character",
            "byte"      : "Byte",
            "long"      : "Long",
            "String"    : "String"
        }

        body = ""
        paramlist = "" # list of variables to pass into the method to test

        i = 0;
        for ptype in parameterTypes:
            # create string assigning variables to the parsed type from the command line
            # int _num = Integer.parseInt(args[i]);
            ptypeCap = ptype.capitalize()
            varName = "_" + str(i)
            if not ptype.startswith("String"):
                body += "\t\t%s %s = %s.parse%s(args[%d]);\n" % (ptype, varName, objNames[ptype], ptypeCap, i)
            else:
                body += "\t\t%s %s = args;\n" % (ptype, varName)
            
            paramlist += varName + ", "
            i += 1

        paramlist = paramlist[0:-2] # strip the ending ", "

        body += "\n"

        if returnType != "void":
            retypeCap  = returnType.capitalize()
            body += "\t\t%s expected = %s.parse%s(args[%d]);\n" % (returnType, objNames[ptype], retypeCap, i)
            body += "\n"
            body += "\t\t%s actual = %s.%s(%s);\n" % (returnType, getClassName(classFilePath), methodName, paramlist)
            body += "\t\tSystem.out.println(expected == actual);"

        else:
            body += "\t\t%s.%s(%s);\n" % (getClassName(classFilePath), methodName, paramlist)

        self.code = '''
public class Svel%s {
    public static void main(String[] args) 
    {
%s
    }
}
''' % (methodName, body)

    '''
    Creates the Java file named Svel<methodName> in the same directory as the
    class file to test
    '''
    def createJavaFile(self):
        absPath = getAbsPath(self.classFilePath)
        array = absPath.split("/")[0:-1]
        absPath = ""
        for dir in array:
            absPath += dir + "/"
        absPath += "Svel%s.java" % (self.methodName)
        svel = open(absPath, "w")
        svel.write(self.code)
        svel.close()
        print "Created %s:\n%s" % (absPath, self.code)

        return absPath
    


#jcreator = Jcreator("../test/java_files/Add.java", "add", ["int", "int"], "int")
#jcreator.createJavaFile()

