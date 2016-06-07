# What is the Python Toolbox? #

The Python Toolbox is a collection of Python tools for various tasks. It
contains:

 - `python_toolbox.caching`: Tools for caching functions, class instances and
   properties.
 
 - `python_toolbox.cute_iter_tools`: Tools for manipulating iterables. Adds
   useful functions not found in Python's built-in `itertools`.
 
 - `python_toolbox.context_management`: Pimping up your context managers.
 
 - `python_toolbox.emitting`: A publisher-subscriber framework that doesn't
   abuse strings.
   
 - And many, *many* more! The Python Toolbox contains **100+** useful little
   tools.

Documentation: http://python-toolbox.readthedocs.io

Python Toolbox on GitHub: https://github.com/cool-RR/python_toolbox

Python Toolbox on PyPI: https://pypi.python.org/pypi/python_toolbox

The Python Toolbox is released under the MIT license.

# Not backward-compatible yet #

Backward compatibility is currently *not* maintained. If you're using Python Toolbox in your code and you want to upgrade to a newer version of Python Toolbox, you'll need to ensure that all the calls to Python Toolbox aren't failing. (A good test suite will usually do the trick.)


# Roadmap #

## Present ##

Python Toolbox is at version 0.9.3. It's being used in production every day, but backward compatibility isn't guaranteed yet.

## Next tasks ##

Adding more useful tools.

## Future ##

Make a 1.0 release and start maintaining backward compatibility.


# Mailing lists #

All general discussion happens at **[the Python Toolbox Google Group](https://groups.google.com/forum/#!forum/python-toolbox)**. If you need help with the Python Toolbox, you're welcome to post your question and we'll try to help you.

The development mailing list is **[python-toolbox-dev](https://groups.google.com/forum/#!forum/python-toolbox-dev)**. This is where we discuss the development of the Python Toolbox itself.

If you want to be informed on new releases of the Python Toolbox, sign up for
**[the low-traffic python-toolbox-announce Google Group](https://groups.google.com/forum/#!forum/python-toolbox-announce)**.

# Python versions #
 
The Python Toolbox supports Python versions 2.7 and 3.3+.

It's tested on both CPython and PyPy 2.1.


# Tests #

Tests can be run by running the `_test_python_toolbox.py` script that's
installed automatically with the Python Toolbox.

When `python_toolbox` isn't installed, you may run `nosetests` at the repo root
to run the tests.


------------------------------------------------------------------

The Python Toolbox was created by Ram Rachum. I provide 
[Development services in Python and Django](https://chipmunkdev.com)


