#!/usr/bin/env python

# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Distribute setup file for garlicsim_wx.
'''

def ensure_Distribute_is_installed():
    
    no_distribute_error = Exception('''`Distribute` is required but is not \
installed. Download it from the internet and install it, then try again.''')

    try:
        import pkg_resources
    except ImportError:
        raise no_distribute_error
    
    pkg_resources.require('Distribute')

ensure_Distribute_is_installed()

import os
import setuptools
import distutils
import garlicsim_wx

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
        name='garlicsim_wx for Python 2.6',
        version=garlicsim_wx.__version__,
        install_requires=['Distribute >= 0.6', 'garlicsim == 0.1.1'],
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