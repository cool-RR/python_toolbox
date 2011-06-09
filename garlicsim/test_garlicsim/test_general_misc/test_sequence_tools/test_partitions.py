# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `sequence_tools.partitions`.'''

from __future__ import with_statement

from garlicsim.general_misc import cute_testing

from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc.sequence_tools import partitions


def test():
    '''Test the basic workings of `partitions`.'''
    r = range(8)
    assert partitions(r, 1) == partitions(r, n_partitions=8) == \
           [[0], [1], [2], [3], [4], [5], [6], [7]]
    assert partitions(r, 2) == partitions(r, n_partitions=4) == \
           [[0, 1], [2, 3], [4, 5], [6, 7]]
    assert partitions(r, 3) == partitions(r, n_partitions=3) == \
           [[0, 1, 2], [3, 4, 5], [6, 7]]
    assert partitions(r, 4) == partitions(r, n_partitions=2) == \
           [[0, 1, 2, 3], [4, 5, 6, 7]]
    assert partitions(r, 5) == [[0, 1, 2, 3, 4], [5, 6, 7]]
    assert partitions(r, 6) == [[0, 1, 2, 3, 4, 5], [6, 7]]
    assert partitions(r, 7) == [[0, 1, 2, 3, 4, 5, 6], [7]]
    assert partitions(r, 8) == partitions(r, 9) == partitions(r, 100) == \
           [[0, 1, 2, 3, 4, 5, 6, 7]] 
    
    
def test_too_many_arguments():
    '''Test `partitions` complains when too many arguments are given.'''
    with cute_testing.RaiseAssertor(text='*either*'):
        partitions([1, 2, 3], 2, 2)

        
def test_allow_remainder():
    '''Test `partitions` complains when there's an unallowed remainder.'''
    r = range(9)
    
    # 9 divides by 1, 3 and 9, so no problems here:
    assert partitions(r, 1, allow_remainder=False) == \
           partitions(r, n_partitions=9, allow_remainder=False) == \
           [[0], [1], [2], [3], [4], [5], [6], [7], [8]]
    assert partitions(r, 3, allow_remainder=False) == \
           partitions(r, n_partitions=3, allow_remainder=False) == \
           [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    
    # ...But now we try 2, 4 and 5 and get exceptions:
    with cute_testing.RaiseAssertor(text='remainder'):
        partitions(r, 2, allow_remainder=False)
    with cute_testing.RaiseAssertor(text='remainder'):
        partitions(r, 4, allow_remainder=False)
    with cute_testing.RaiseAssertor(text='remainder'):
        partitions(r, 5, allow_remainder=False)
    with cute_testing.RaiseAssertor(text='remainder'):
        partitions(r, n_partitions=2, allow_remainder=False)
    with cute_testing.RaiseAssertor(text='remainder'):
        partitions(r, n_partitions=4, allow_remainder=False)
    with cute_testing.RaiseAssertor(text='remainder'):
        partitions(r, n_partitions=5, allow_remainder=False)
        