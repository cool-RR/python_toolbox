#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Setuptools setup file for garlicsim.'''

import os
import setuptools
import sys


### Ensuring correct Python version: ##########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception('This package is not compatible with Python 3.x. Use '
                    '`garlicsim_py3` instead.')
if sys.version_info[1] <= 4:
    raise Exception('This package requires Python 2.5 and upwards. (Not '
                    'including 3.x).')
#                                                                             #
### Finished ensuring correct Python version. #################################


def get_garlicsim_packages():
    '''
    Get all the packages in `garlicsim`.
    
    Returns something like:
    
        ['garlicsim', 'garlicsim.misc',
        'garlicsim.general_misc.nifty_collections', ... ]
        
    '''
    return ['garlicsim.' + p for p in
            setuptools.find_packages('./garlicsim')] + \
           ['garlicsim']


def get_test_garlicsim_packages():
    '''
    Get all the packages in `test_garlicsim`.
    
    Returns something like:
    
        ['test_garlicsim', 'test_garlicsim.test_misc',
        'test_garlicsim.test_general_misc.test_nifty_collections', ... ]
        
    '''
    return ['test_garlicsim.' + p for p in
            setuptools.find_packages('./test_garlicsim')] + \
           ['test_garlicsim']


def get_packages():
    '''
    Get all the packages in `garlicsim` and `test_garlicsim`.
    
    Returns something like:
    
        ['test_garlicsim', 'garlicsim', 'garlicsim.misc',
        'test_garlicsim.test_general_misc.test_nifty_collections', ... ]
        
    '''
    return get_garlicsim_packages() + get_test_garlicsim_packages()


my_long_description = \
'''\
GarlicSim is a platform for writing, running and analyzing simulations.

It can handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.org for more info.
'''

my_classifiers = [
    'Development Status :: 4 - Beta',
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
    name='garlicsim',
    version='0.6.3',
    requires=['distribute'],
    test_suite='nose.collector',
    install_requires=['distribute'],
    tests_require=['nose>=1.0.0'],
    description='Pythonic framework for working with simulations',
    author='Ram Rachum',
    author_email='ram@rachum.com',
    url='http://garlicsim.org',
    packages=get_packages(),
    scripts=['garlicsim/scripts/start_simpack.py',
             'test_garlicsim/scripts/_test_garlicsim.py'],
    license='LGPL v2.1',
    long_description = my_long_description,
    classifiers = my_classifiers,
    include_package_data = True,
    zip_safe=False,
)

