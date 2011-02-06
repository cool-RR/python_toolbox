#!/usr/bin/env python
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

import os.path
import zipfile

# tododoc: helpful error messages:
assert __name__ == '__main__'
assert os.path.realpath('.') == \
       os.path.realpath(os.path.join(os.getcwd(), 'misc', 'testing', 'zip'))

# todo: define function for zipping a folder, then use it to make garlicsim,
# garlicsim_lib and garlicsim_wx in build folder
