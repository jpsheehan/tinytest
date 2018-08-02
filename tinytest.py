""" tinytest.py

A simple testing framework written in Python3 and licensed under GNU GPLv3.

Simply create a test file and add test cases similar to Python's doctests.

Run tinytest like so:

    python3 tinytest.py [filename]

If the filename is ommitted, it will default to "Testfile".

The exit status code will be:
- 0: When no failures have taken place.
- 255: When an error occurred reading the test file.
- otherwise: The number of tests that failed.

Example test file (indented for clarity):

    Lines before the first test definition are ignored.

    Just like Python's doctests, a test definition begins with three consecutive greater-than symbols at the start of a line. The rest of the line defines the command to be run. You can use pipes and redirection as per usual.

    >>> echo "Hello, World!"
    Hello, World!
    >>> echo "Cool" > cool && cat cool && rm cool
    Cool


"""

import difflib
import os
import subprocess
import sys

DEFAULT_TESTFILE_NAME = "Testfile"

def test(command, expected_output, silent=False):
    """ Runs a single test.
    A test is defined by the command to be run and the expected output.
    If silent is true no output will be printed.
    Returns true if the test passed.
    Otherwise an error message is printed and false is returned. """

    # run the command as a shell process, reading the output into proc_out
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    proc_out, _ = proc.communicate()
    proc_out = proc_out.decode("utf8")

    # return true if the expected_output matches proc_out
    if expected_output == proc_out:
        return True
    
    if not silent:

        # get the differences between the expected output and actual output
        diffs = difflib.Differ().compare(expected_output.splitlines(1), \
            proc_out.splitlines(1))

        # print an error message followed by the diff message
        print("*** \"{0}\" failed. See diff below: ***\n".format(command))
        print(''.join(list(diffs)) + "\n")
    
    # return false because the test didn't pass
    return False

def testall(tests, silent=False):
    """ Prints information about a list of tests that have been run.
    If silent is true, no output will be printed.
    Returns a tuple in the format (failures, successes, total)"""

    # get the number of failures and successes
    failures = len([_ for _ in tests if not _])
    successes = len(tests) - failures

    if not silent:

        # print a short message detailing how many tests passed
        print("*** Passed {0}/{1} tests ***".format(successes, len(tests)))

    # return information about how many tests passed and failed
    return (failures, successes, len(tests))

def readTestFile(filename):
    """ Attempt to read the test file.
    Returns a list of tuples in the form (command, expected_output)."""
    tests = []

    with open(testfile_name, "r") as f:

        line = f.readline()
        while line != "":

            # create a new test
            if line.startswith(">>>"):
                tests.append([line[3:].strip(), ""])

            # add a line of expected output to the newest test
            elif len(tests) > 0:
                tests[len(tests)-1][1] += line
        
            line = f.readline()
    
    return [(t[0], t[1]) for t in tests]

if __name__ == "__main__":

    # either use the default filename "Testfile" or use the one
    # passed in to the command line
    testfile_name = DEFAULT_TESTFILE_NAME
    if len(sys.argv) >= 2:
        testfile_name = sys.argv[1]

    try:
        # get the tests
        tests = readTestFile(testfile_name)

        # run all the tests
        results = testall([test(t[0], t[1]) for t in tests])

        # exit, setting the status code to the number of failed tests
        exit(results[0])

    # print an error and exit if the file could not be read
    except Exception:
        print("*** an error occurred reading \"{0}\" ***".format(testfile_name))
        exit(255)
