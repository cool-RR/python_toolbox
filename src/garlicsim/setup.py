#!/usr/bin/env python

import os
from distutils.core import setup
from general_misc import package_finder

my_long_description = \
'''\
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.
'''

my_packages = package_finder.get_packages('', include_self=True,
                                          recursive=True)

print(my_packages)

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