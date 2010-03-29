#!/usr/bin/env python

# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Setuptools setup file for garlicsim_wx.
'''

import os
import setuptools
import distutils # Just for deleting the "build" directory.

try:
    distutils.dir_util.remove_tree('build', verbose=True)
except Exception:
    pass

def get_packages():
    return ['garlicsim_wx.' + p for p
            in setuptools.find_packages('./garlicsim_wx')] + \
           ['garlicsim_wx']

my_long_description = \
'''\
garlicsim_wx, a wxPython GUI for garlicsim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.
'''

my_classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Topic :: Scientific/Engineering',
]



setuptools.setup(
    name='garlicsim_wx',
    version='0.3',
    requires=['garlicsim (== 0.3)'],
    install_requires=['garlicsim == 0.3'],
    description='Gui for garlicsim, a Pythonic framework for working with simulations',
    author='Ram Rachum',
    author_email='cool-rr@cool-rr.com',
    url='http://garlicsim.org',
    packages=get_packages(),
    license="Proprietary",
    long_description = my_long_description,
    classifiers = my_classifiers,
    include_package_data = True,
)
