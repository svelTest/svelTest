# =============================================================================
# pfileutil.py
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


def getAbsPath(relPath):
	''' Returns the absolute path from the relative path
	relPath - the relative path to the file (from pwd)'''

	# from jfileutil -- TODO: DRY...
	slash = "/"
	if os.name == "nt":
		slash = "\\"
	cwdArray = os.getcwd().split(slash)[1:]
	if relPath[0] == slash:
		return relPath
	relPathArray = relPath.split(slash)
	while relPathArray[0] == "..":
		cwdArray = cwdArray[0 : len(cwdArray) - 1]
		relPathArray = relPathArray[1:]
	absPathArray = cwdArray + relPathArray
	absPath = ""
	for dir in absPathArray:
		absPath += slash + dir
	return absPath

def getAbsDir(path):
	''' Return the absolute path to the directory of the file
	path - the absolute or relative path to the file
	'''

	# from jfileutil -- TODO: DRY...
	slash = "/"
	if os.name == "nt":
		slash = "\\"
	absPath = getAbsPath(path)
	array = absPath.split(slash)[0:-1]
	absPath = ""
	for dir in array:
		absPath += dir + slash
	return absPath

def getClassName(classFilePath):
	''' Return the Python class name from the file path
	classFilePath - the absolute or relative path to the file
	'''

	# from jfileutil -- TODO: DRY...
	slash = "/"
	if os.name == "nt":
		slash = "\\"
	# get "Add" from rel/path/to/Add.py
	return classFilePath.split(slash)[-1][0:-3]