#!/usr/bin/env python

# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Distribute setup file for garlicsim.
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
import garlicsim

try:
    distutils.dir_util.remove_tree('build', verbose=True)
except Exception:
    pass

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
    'Programming Language :: Python :: 2.5',
    'Topic :: Scientific/Engineering',
    'Programming Language :: Python',
]

try:
    setuptools.setup(
        name='garlicsim for Python 2.5',
        version=garlicsim.__version__,
        install_requires=['Distribute >= 0.6'],
        description='Pythonic framework for working with simulations',
        author='Ram Rachum',
        author_email='cool-rr@cool-rr.com',
        url='http://garlicsim.org',
        packages=setuptools.find_packages(),
        license="LGPL v2.1",
        long_description = my_long_description,
        classifiers = my_classifiers,
        include_package_data = True,
    )
    

finally:
    
    try:
        distutils.dir_util.remove_tree('build', verbose=True)
    except Exception:
        pass