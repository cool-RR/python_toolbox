# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for working with garbage-collection.'''

import gc

from python_toolbox import sys_tools

def collect():
    '''
    Garbage-collect any items that don't have any references to them anymore.
    '''
    if sys_tools.is_pypy:
        for _ in range(3):
            gc.collect()
    else:
        gc.collect()