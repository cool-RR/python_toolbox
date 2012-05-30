# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import gc

from python_toolbox import sys_tools

def collect():
    if sys_tools.is_pypy:
        for i in range(3):
            gc.collect()
    else:
        gc.collect()