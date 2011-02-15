# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.cute_iter_tools.shorten`.'''

import nose.tools

from garlicsim.general_misc.sequence_tools import combinations


def test():
    '''Test basic workings of `combinations`.'''
    my_range = [0, 1, 2, 3, 4]
    
    
    assert list(combinations([1, 2, 3, 4], n=2)) == [
        [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]
    ]
    
    assert list(combinations(range(4), 3)) == [
        [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]
    ]
    
    
def test_all_sizes():
    list(combinations(range(4)))
    assert False # blocktodo