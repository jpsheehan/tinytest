tinytest
========

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

