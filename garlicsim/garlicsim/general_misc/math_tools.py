# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines math-related tools.'''

from __future__ import division

def sign(x):
    '''Get the sign of a number.'''
    if x > 0:
        return 1
    if x == 0:
        return 0
    assert x < 0
    return -1

def round_to_int(x, up=False):
    rounded_down = int(x // 1)
    if up:
        return int(x) if x.is_integer() else rounded_down + 1
    else:
        return rounded_down
