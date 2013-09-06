#!/usr/bin/env python

# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Setuptools setup file for `python_toolbox`.'''

import os
import setuptools
import sys

### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception("Python 3.x is not supported, only Python 2.6 and Python "
                    "2.7.")
if sys.version_info[1] <= 5:
    raise Exception(
        "You're using Python <= 2.5, but this package requires either Python "
        "2.6 or Python 2.7, so you can't use it unless you upgrade your "
        "Python version."
    )
#                                                                             #
### Finished confirming correct Python version. ###############################

def get_python_toolbox_packages():
    '''
    Get all the packages in `python_toolbox`.
    
    Returns something like:
    
        ['python_toolbox', 'python_toolbox.caching',
        'python_toolbox.nifty_collections', ... ]
        
    '''
    return ['python_toolbox.' + p for p in
            setuptools.find_packages('./python_toolbox')] + \
           ['python_toolbox']


def get_test_python_toolbox_packages():
    '''
    Get all the packages in `test_python_toolbox`.
    
    Returns something like:
    
        ['test_python_toolbox', 'test_python_toolbox.test_caching',
        'test_python_toolbox.test_nifty_collections', ... ]
        
    '''
    return ['test_python_toolbox.' + p for p in
            setuptools.find_packages('./test_python_toolbox')] + \
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

Documentation: http://python-toolbox.readthedocs.org

GitHub: https://github.com/cool-RR/python_toolbox

CI server: https://jenkins.shiningpanda.com/python-toolbox/job/python_toolbox/

Roadmap
=======

Present
-------

Python Toolbox is at version 0.5.1, which is an alpha release. It's being used in production every day, but backward compatibility isn't guaranteed yet.

Next tasks
----------

Making Python Toolbox support Python 3.x, and the packaging arrangements necessary.

Adding more useful tools.

Future
------

Make a 1.0 release and start maintaining backward compatibility.
'''

my_classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers', 
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent', 
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]


setuptools.setup(
    name='python_toolbox',
    version='0.5.1',
    requires=['distribute'],
    test_suite='nose.collector',
    install_requires=['distribute'],
    tests_require=['nose>=1.0.0',
                   'docutils>=0.8'],
    description='A collection of Python tools for various tasks',
    author='Ram Rachum',
    author_email='ram@rachum.com',
    packages=get_packages(),
    scripts=['test_python_toolbox/scripts/_test_python_toolbox.py'],
    long_description=my_long_description,
    license='MIT',
    classifiers=my_classifiers,
    include_package_data=True,
    zip_safe=False,
)

