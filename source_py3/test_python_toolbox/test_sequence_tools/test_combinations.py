# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.sequence_tools.combinations`.'''

import nose.tools

from python_toolbox.sequence_tools import combinations
from python_toolbox import sequence_tools


def test():
    '''Test basic workings of `combinations`.'''
    my_range = [0, 1, 2, 3, 4]
    
    
    assert list(combinations(range(4), n=2)) == [
        [0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]
    ]
    
    assert list(combinations(range(4), 3)) == [
        [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]
    ]
    
    assert tuple(combinations('meowfrr', 5)) == (
        ['m', 'e', 'o', 'w', 'f'], ['m', 'e', 'o', 'w', 'r'],
        ['m', 'e', 'o', 'w', 'r'], ['m', 'e', 'o', 'f', 'r'],
        ['m', 'e', 'o', 'f', 'r'], ['m', 'e', 'o', 'r', 'r'],
        ['m', 'e', 'w', 'f', 'r'], ['m', 'e', 'w', 'f', 'r'],
        ['m', 'e', 'w', 'r', 'r'], ['m', 'e', 'f', 'r', 'r'],
        ['m', 'o', 'w', 'f', 'r'], ['m', 'o', 'w', 'f', 'r'],
        ['m', 'o', 'w', 'r', 'r'], ['m', 'o', 'f', 'r', 'r'],
        ['m', 'w', 'f', 'r', 'r'], ['e', 'o', 'w', 'f', 'r'],
        ['e', 'o', 'w', 'f', 'r'], ['e', 'o', 'w', 'r', 'r'],
        ['e', 'o', 'f', 'r', 'r'], ['e', 'w', 'f', 'r', 'r'],
        ['o', 'w', 'f', 'r', 'r']
    )
    
    assert list(combinations(range(5), n=2, start=2)) == \
           list(combinations(range(2, 5), n=2))
    
    
def test_all_sizes():
    '''Test using `n=None` so combinations of all sizes are returned.'''
    assert list(combinations(range(4))) == sequence_tools.flatten(
        list(combinations(range(4), i)) for i in range(1, 4+1)
    )