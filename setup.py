#!/usr/bin/env python

# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Setuptools setup file for `python_toolbox`.'''

import os
import re
import setuptools
import sys

def read_file(filename):
    with open(filename) as file:
        return file.read()

version = re.search("__version__ = '([0-9.]*)'",
                    read_file('python_toolbox/__init__.py')).group(1)



def get_python_toolbox_packages():
    '''
    Get all the packages in `python_toolbox`.

    Returns something like:

        ['python_toolbox', 'python_toolbox.caching',
        'python_toolbox.nifty_collections', ... ]

    '''
    return ['python_toolbox.' + p for p in
            setuptools.find_packages('python_toolbox')] + \
           ['python_toolbox']


def get_test_python_toolbox_packages():
    '''
    Get all the packages in `test_python_toolbox`.

    Returns something like:

        ['test_python_toolbox', 'test_python_toolbox.test_caching',
        'test_python_toolbox.test_nifty_collections', ... ]

    '''
    return ['test_python_toolbox.' + p for p in
            setuptools.find_packages('test_python_toolbox')] + \
           ['test_python_toolbox']


def get_packages():
    '''
    Get all the packages in `python_toolbox` and `test_python_toolbox`.

    Returns something like:

        ['test_python_toolbox', 'python_toolbox', 'python_toolbox.caching',
        'test_python_toolbox.test_nifty_collections', ... ]

    '''
    return get_python_toolbox_packages() + get_test_python_toolbox_packages()


my_long_description = \
'''\

The Python Toolbox is a collection of Python tools for various tasks. It
contains:

 - ``python_toolbox.caching``: Tools for caching functions, class instances and
    properties.

 - ``python_toolbox.cute_iter_tools``: Tools for manipulating iterables. Adds
    useful functions not found in Python's built-in ``itertools``.

 - ``python_toolbox.context_management``: Pimping up your context managers.

 - ``python_toolbox.emitting``: A publisher-subscriber framework that doesn't
    abuse strings.

 - And many, *many* more! The Python Toolbox contains **100+** useful
   little tools.


Documentation: http://python-toolbox.readthedocs.io

Python Toolbox on GitHub: https://github.com/cool-RR/python_toolbox

Python Toolbox on PyPI: https://pypi.python.org/pypi/python_toolbox

Tests
=====

Test can be run by running the ``_test_python_toolbox.py`` script that's
installed automatically with the Python Toolbox.

When ``python_toolbox`` isn't installed, you may run ``pytest`` at the repo
root to run the tests.


-------------------------------------------------------

The Python Toolbox was created by Ram Rachum. I provide
`Development services in Python and Django <https://chipmunkdev.com>`_.


'''

my_classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]


install_requires = ['setuptools']

try:
    from setuptools.command.test import test as TestCommand
except ImportError:
    # This setuptools is deprecated so it may be removed in the future.
    PyTest = None
else:
    class PyTest(TestCommand):
        # user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

        def initialize_options(self):
            TestCommand.initialize_options(self)
            self.pytest_args = []

        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            import pytest
            errno = pytest.main(self.pytest_args)
            sys.exit(errno)



setuptools.setup(
    name='python_toolbox',
    version=version,
    install_requires=install_requires,
    description='A collection of Python tools for various tasks',
    author='Ram Rachum',
    author_email='ram@rachum.com',
    package_dir={'': '.'},
    packages=get_packages(),
    scripts=['test_python_toolbox/scripts/_test_python_toolbox.py'],
    entry_points={
        'console_scripts': [
            '_test_python_toolbox = test_python_toolbox:invoke_tests',
        ],
    },
    long_description=my_long_description,
    license='MIT',
    classifiers=my_classifiers,
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'tests': {
            'pytest',
            'docutils>=0.8',
        },
    },
    cmdclass=({'test': PyTest,} if PyTest is not None else {})

)

