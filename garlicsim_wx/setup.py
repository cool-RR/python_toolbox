#!/usr/bin/env python

# Copyright 2009 Ram Rachum.
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
    'Programming Language :: Python :: 2.6',
    'Topic :: Scientific/Engineering',
    'Programming Language :: Python',
]


try:
    
    setuptools.setup(
        name='garlicsim_wx for Python 2.5',
        version='0.1.5',
        requires=['garlicsim (== 0.1.5)'],
        install_requires=['garlicsim == 0.1.5'],
        description='Gui for garlicsim, a Pythonic framework for working with simulations',
        author='Ram Rachum',
        author_email='cool-rr@cool-rr.com',
        url='http://garlicsim.org',
        packages=setuptools.find_packages(),
        license="Proprietary",
        long_description = my_long_description,
        classifiers = my_classifiers,
        include_package_data = True,
    )


finally:
    
    try:
        distutils.dir_util.remove_tree('build', verbose=True)
    except Exception:
        pass