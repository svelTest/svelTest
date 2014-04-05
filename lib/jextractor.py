import os, sys, subprocess

class Jextractor(object):

    '''
    Gets the method signature to test from the specified file.
        file - "rel/path/to/file"
        name - name of method to test
        params - array of reslang keywords
    '''
    def getMethodSignature(self, file, name, params):
        regexp_params = ""
        for p in params:
            strip_p = p.split("_")[1]; # strip type from j_type
            # regexp for parameters - 0 or more spaces, followed by type, 
            # followed by 1 or more spaces, followed by a comma 
            regexp_params += "[ ]*%s[ ]\+.*," % (strip_p)
        regexp_params = regexp_params[0 : len(regexp_params)-1] # take off the extra comma

        # one or more spaces, followed by method name, followed by 0 or more spaces
        # followed by open paren, followed by RE for params, and finally a close paren
        regexp = "[ ]\+%s[ ]*(%s)" % (name, regexp_params)
        grep = "grep \'%s\' %s" % (regexp, file) # grep command
        output = subprocess.check_output(grep, shell=True)

        return output.strip() # strip leading/trailing whitespace

    '''
    Gets the return type of the method to test.
        file - "rel/path/to/file"
        name - name of method to test
        params - array of reslang keywords
    '''
    def getMethodRetType(self, file, name, params):
        sig = self.getMethodSignature(file, name, params)
        sigArray = sig.split(" ")
        i = 0
        while i < len(sigArray):
            if sigArray[i].startswith(name):
                break
            i += 1

        # return type will be the word on the left side of the method name
        return sigArray[i - 1]


'''
Example: extract the add() method in Add.java
'''
f = "../test/java_files/Add.java"
name = "add"
params = ["j_int", "j_int"]

extractor = Jextractor()
# Get full method signature
sig = extractor.getMethodSignature(f, name, params)
print "Method signature: " + sig

# Get return type of add()
ret = extractor.getMethodRetType(f, name, params)
print "Return type: " + ret