#!/usr/bin/env python

# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Distutils setup file for GarlicSim.
'''

import os
from distutils.core import setup
import distutils
from general_misc import package_finder

try:
    distutils.dir_util.remove_tree('build', verbose=True)
except:
    pass

my_long_description = \
'''\
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.
'''

my_packages = package_finder.get_packages('', include_self=True,
                                          recursive=True)

setup(
    name='GarlicSim',
    version='0.1',
    description='A Pythonic framework for working with simulations',
    author='Ram Rachum',
    author_email='cool-rr@cool-rr.com',
    url='http://garlicsim.org',
    packages=my_packages,
    package_dir={'': '..'},
    license= "LGPL 2.1 License",
    long_description = my_long_description,
        
)

try:
    distutils.dir_util.remove_tree('build', verbose=True)
except:
    pass