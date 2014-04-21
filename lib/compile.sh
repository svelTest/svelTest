#!/bin/bash
# =============================================================================
# compile.sh
# 
# Shell script to facilitate compilation of svelTest programs
#     Input:  The relative path to a svelTest program
#     Usage:  ./compile.sh <path_to_svelTest_program>
#
# -----------------------------------------------------------------------------
# Columbia University, Spring 2014
# COMS 4115: Programming Languages & Translators, Prof. Aho
#     svelTest team:
#     Emily Hsia, Kaitlin Huben, Josh Lieberman, Chris So, Mandy Swinton
# =============================================================================

# if the user runs the script wihtout any arguments
if [ "$#" == "0" ]; then
    echo "Usage: ./compile.sh [-v] <file_to_compile>.svel"
    exit 1
fi

# running the compiler without the verbose flag
if [ "$#" == "1" ]; then
	# input from user
    RELATIVE_PATH=$1
    # verbose
    VERBOSE="no"
fi

# running the compiler with the verbose flag
if [ "$#" -eq "2" ]; then
    if [ $1 == '-v' ]; then
    # verbose
	VERBOSE=$1
	# input from the user
	RELATIVE_PATH=$2
	fi
fi

# if input is ../test/java_files/fibTester.svel,
# DIRECTORY_PATH = ../test/java_files
# FILENAME = fibTester.svel

DIRECTORY_PATH=`dirname $RELATIVE_PATH`
FILENAME=`basename $RELATIVE_PATH`

echo "Copying $FILENAME into lib for compiling..."
echo " "
cp $RELATIVE_PATH ./

echo "Attempting to compile..."
if [ $VERBOSE == "no" ]; then
	# run compiler without passing flag
	python svelCompile.py $FILENAME
else
	# need to pass flag to compiler
	python svelCompile.py $VERBOSE $FILENAME
fi

echo " "
echo "Removing copy of $FILENAME from lib..."
rm -rf $FILENAME

# figure out what name of compiled file should be
# Split *.svel filename to get *.py
NAME=`echo "$FILENAME" | cut -d'.' -f1`
COMPILED_NAME="$NAME.py"

if [ -e $COMPILED_NAME ]; then
	# compilation occurred successfully
	echo "Moving compiled file back to $FILENAME's directory..."
	mv $COMPILED_NAME $DIRECTORY_PATH/
	echo " "
	echo "Compilation complete! You can go to $DIRECTORY_PATH and run $COMPILED_NAME any time."
else
	echo " "
	echo "Compilation failed; please check the error messages and try again."
fi