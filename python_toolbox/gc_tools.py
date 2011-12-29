# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import gc

from garlicsim.general_misc import sys_tools

def collect():
    if sys_tools.is_pypy:
        for i in range(3):
            gc.collect()
    else:
        gc.collect()