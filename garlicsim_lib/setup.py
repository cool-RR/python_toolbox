#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Setuptools setup file for garlicsim_lib.'''

import os
import sys
import setuptools


### Ensuring correct Python version: ##########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception('This package is not compatible with Python 3.x. Use '
                    '`garlicsim_lib_py3` instead.')
if sys.version_info[1] <= 4:
    raise Exception('This package requires Python 2.5 and upwards. (Not '
                    'including 3.x).')
#                                                                             #
### Finished ensuring correct Python version. #################################


def get_garlicsim_lib_packages():
    '''
    Get all the packages in `garlicsim_lib`.
    
    Returns something like:
    
        ['garlicsim_lib', 'garlicsim_lib.simpacks',
        'garlicsim_lib.simpacks.life', ... ]
        
    '''
    return ['garlicsim_lib.' + p for p in
            setuptools.find_packages('./garlicsim_lib')] + \
           ['garlicsim_lib']


def get_test_garlicsim_lib_packages():
    '''
    Get all the packages in `test_garlicsim_lib`.
    
    Returns something like:
    
        ['test_garlicsim_lib', 'test_garlicsim_lib.test_simpacks', ...]
        
    '''
    return ['test_garlicsim_lib.' + p for p in
            setuptools.find_packages('./test_garlicsim_lib')] + \
           ['test_garlicsim_lib']


def get_packages():
    '''
    Get all the packages in `garlicsim_lib` and `test_garlicsim_lib`.
    
    Returns something like:
    
        ['test_garlicsim_lib', 'garlicsim_lib', 'garlicsim_lib.simpacks',
        'test_garlicsim_lib.test_simpacks', ... ]
        
    '''
    return get_garlicsim_lib_packages() + get_test_garlicsim_lib_packages()


my_long_description = \
'''\
Collection of GarlicSim simulation packages, for various scientific fields.

To be used with `garlicsim` and possibly `garlicsim_wx`.

Visit http://garlicsim.org for more info.
'''

my_classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    ('License :: OSI Approved :: GNU Library or Lesser General '
     'Public License (LGPL)'),
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering',
]


setuptools.setup(
    name='garlicsim_lib',
    version='0.6.3',
    requires=['garlicsim (== 0.6.3)'],
    install_requires=['garlicsim == 0.6.3'],
    tests_require=['nose>=1.0.0'],
    description='Collection of GarlicSim simulation packages',
    author='Ram Rachum',
    author_email='ram@rachum.com',
    url='http://garlicsim.org',
    packages=get_packages(),
    scripts=['test_garlicsim_lib/scripts/_test_garlicsim_lib.py'],
    license='LGPL v2.1',
    long_description = my_long_description,
    classifiers = my_classifiers,
    include_package_data = True,
    zip_safe=False,
)

