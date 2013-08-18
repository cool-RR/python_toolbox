# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.get_consecutive_subsequences`.'''

from python_toolbox import cute_testing
from python_toolbox import sequence_tools

from python_toolbox.cute_iter_tools import get_consecutive_subsequences


def test():
    '''Test basic workings of `cute_iter_tools.get_consecutive_subsequences`.'''
    
    # `consecutive_pairs` returns an iterator, not a sequence:
    assert not sequence_tools.is_sequence(get_consecutive_subsequences(range(4)))
                                          
    assert tuple(get_consecutive_subsequences(range(4))) == \
           tuple(get_consecutive_subsequences(xrange(4))) == \
           ((0, 1), (1, 2), (2, 3))
                                          
    assert tuple(get_consecutive_subsequences(range(4), wrap_around=True)) == \
           tuple(get_consecutive_subsequences(xrange(4), wrap_around=True)) == \
           ((0, 1), (1, 2), (2, 3), (3, 0))
                                          
    assert tuple(get_consecutive_subsequences('meow')) == \
           (('m', 'e'), ('e', 'o'), ('o', 'w'))
    
    assert tuple(get_consecutive_subsequences([1], wrap_around=True)) == \
           ((1, 1),)
           
           