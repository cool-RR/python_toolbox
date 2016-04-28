#!/usr/bin/env python

# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Setuptools setup file for `python_toolbox`.'''

import os
import setuptools
import sys

### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[:2] <= (2, 5):
    raise Exception(
        "You're using Python <= 2.5, but this package requires either Python "
        "2.6/2.7, or 3.3 or above, so you can't use it unless you upgrade "
        "your Python version."
    )
if sys.version_info[0] == 3 and sys.version_info[1] <= 2:
    raise Exception(
        "You're using Python <= 3.2, but this package requires either Python "
        "3.3 or above, or Python 2.6/2.7, so you can't use it unless you "
        "upgrade your Python version."
    )
#                                                                             #
### Finished confirming correct Python version. ###############################

if sys.version_info[0] == 3:
    source_folder = 'source_py3'
else:
    source_folder = 'source_py2'


def get_python_toolbox_packages():
    '''
    Get all the packages in `python_toolbox`.
    
    Returns something like:
    
        ['python_toolbox', 'python_toolbox.caching',
        'python_toolbox.nifty_collections', ... ]
        
    '''
    return ['python_toolbox.' + p for p in
            setuptools.find_packages('%s/python_toolbox' % source_folder)] + \
           ['python_toolbox']


def get_test_python_toolbox_packages():
    '''
    Get all the packages in `test_python_toolbox`.
    
    Returns something like:
    
        ['test_python_toolbox', 'test_python_toolbox.test_caching',
        'test_python_toolbox.test_nifty_collections', ... ]
        
    '''
    return ['test_python_toolbox.' + p for p in
            setuptools.find_packages('%s/test_python_toolbox'
                                                          % source_folder)] + \
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

   
Please keep in mind that Python Toolbox is still in alpha stage, and that
backward compatibility would *not* be maintained in this phase.

Documentation: http://python-toolbox.readthedocs.io

Python Toolbox on GitHub: https://github.com/cool-RR/python_toolbox

Python Toolbox on PyPI: https://pypi.python.org/pypi/python_toolbox

Tests
=====

Test can be run by running the ``_test_python_toolbox.py`` script that's
installed automatically with the Python Toolbox.

When ``python_toolbox`` isn't installed, you may run ``nosetests`` at the repo
root to run the tests.


Roadmap
=======

Present
-------

Python Toolbox is at version 0.9.2, which is an alpha release. It's being used 
in production every day, but backward compatibility isn't guaranteed yet.

Next tasks
----------

Adding more useful tools.

Future
------

Make a 1.0 release and start maintaining backward compatibility.

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
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]


install_requires = ['setuptools']
    

setuptools.setup(
    name='python_toolbox',
    version='0.9.2',
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=['nose>=1.0.0',
                   'docutils>=0.8'],
    description='A collection of Python tools for various tasks',
    author='Ram Rachum',
    author_email='ram@rachum.com',
    package_dir={'': source_folder}, 
    packages=get_packages(),
    scripts=['%s/test_python_toolbox/scripts/_test_python_toolbox.py'
                                                              % source_folder],
    entry_points={
        'console_scripts': [
            '_test_python_toolbox = test_python_toolbox:invoke_nose',
        ],
    }, 
    long_description=my_long_description,
    license='MIT',
    classifiers=my_classifiers,
    include_package_data=True,
    zip_safe=False,
)

