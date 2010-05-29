#!/usr/bin/env python

# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Setuptools setup file for garlicsim_lib.'''

import os
import sys
import setuptools


if sys.version_info[0] >= 3:
    raise Exception('''This package is not compatible with Python 3.x. Use \
`garlicsim_lib_py3` instead.''')
if sys.version_info[1] <= 4:
    raise Exception('''This package requires Python 2.5 and upwards. (Not \
including 3.x).''')


def get_packages():
    return ['garlicsim_lib.' + p for p in
            setuptools.find_packages('./garlicsim_lib')] + \
           ['garlicsim_lib']

my_long_description = \
'''\
A collection of GarlicSim simulation packages, for various scientific fields.

To be used with `garlicsim` and possibly `garlicsim_wx`.

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
    name='garlicsim_lib',
    version='0.5',
    requires=['garlicsim (== 0.5)'],
    install_requires=['garlicsim == 0.5'],
    description='Collection of GarlicSim simulation packages',
    author='Ram Rachum',
    author_email='cool-rr@cool-rr.com',
    url='http://garlicsim.org',
    packages=get_packages(),
    license='LGPL v2.1',
    long_description = my_long_description,
    classifiers = my_classifiers,
    include_package_data = True,
    zip_safe=False,
)

