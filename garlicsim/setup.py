#!/usr/bin/env python

# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Setuptools setup file for garlicsim.
'''

import os
import setuptools
import distutils # Just for deleting the "build" directory.

try:
    distutils.dir_util.remove_tree('build', verbose=True)
except Exception:
    pass

def get_packages():
    return ['garlicsim.' + p for p in setuptools.find_packages('./garlicsim')]

my_long_description = \
'''\
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.org for more info.
'''

my_classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Topic :: Scientific/Engineering',
]


setuptools.setup(
    name='garlicsim',
    version='0.3',
    description='Pythonic framework for working with simulations',
    author='Ram Rachum',
    author_email='cool-rr@cool-rr.com',
    url='http://garlicsim.org',
    packages=get_packages(),
    license="LGPL v2.1",
    long_description = my_long_description,
    classifiers = my_classifiers,
    include_package_data = True,
)

