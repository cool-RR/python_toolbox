# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import garlicsim.general_misc.cute_iter_tools as cute_iter_tools

def all_equal(iterable):
    return all(a==b for (a, b) in cute_iter_tools.pairs(iterable))