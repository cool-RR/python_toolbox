# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `logic_tools.all_equal`.'''

import itertools

from garlicsim.general_misc.logic_tools import logic_max


def test():
    '''Test the basic working of `logic_max`.'''
    assert logic_max(range(4)) == 3
    assert logic_max(set(range(5))) == 4
    1/0