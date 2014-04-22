# =============================================================================
# cfileutil.py
# 
# Provides helper functions to get information from file paths
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

import os

'''
Gets the absolute path to the file
    relPath - relative path (from pwd) to the file
'''
def getAbsPath(relPath):
    cwdArray = os.getcwd().split("/")[1:]
    if relPath[0] == "/":
        return relPath
    relPathArray = relPath.split("/")
    while relPathArray[0] == "..":
        cwdArray = cwdArray[0 : len(cwdArray) - 1]
        relPathArray = relPathArray[1:]
    absPathArray = cwdArray + relPathArray
    absPath = ""
    for dir in absPathArray:
        absPath += "/" + dir
    return absPath

'''
Gets the absolute path to the directory the file lives in
    path - absolute or relative path to the file
'''
def getAbsDir(path):
    absPath = getAbsPath(path)
    array = absPath.split("/")[0:-1]
    absPath = ""
    for dir in array:
        absPath += dir + "/"
    return absPath

'''
Get the C class name from the file path
    classFilePath - relative or absolute path to the file
'''
def getClassName(classFilePath):
    # get "Add" from rel/path/to/Add.c
    return classFilePath.split("/")[-1][0:-2]