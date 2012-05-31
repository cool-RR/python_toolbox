# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.consecutive_pairs`.'''

from python_toolbox import cute_testing
from python_toolbox import sequence_tools

from python_toolbox.cute_iter_tools import consecutive_pairs


def test():
    '''Test the basic workings of `consecutive_pairs`.'''
    # `consecutive_pairs` returns an iterator, not a sequence:
    assert not sequence_tools.is_sequence(consecutive_pairs(range(4)))
                                          
    assert tuple(consecutive_pairs(range(4))) == \
           tuple(consecutive_pairs(xrange(4))) == \
           ((0, 1), (1, 2), (2, 3))
                                          
    assert tuple(consecutive_pairs(range(4), wrap_around=True)) == \
           tuple(consecutive_pairs(xrange(4), wrap_around=True)) == \
           ((0, 1), (1, 2), (2, 3), (3, 0))
                                          
    assert tuple(consecutive_pairs('meow')) == \
           (('m', 'e'), ('e', 'o'), ('o', 'w'))
    
    assert tuple(consecutive_pairs([1], wrap_around=True)) == \
           ((1, 1),)
           
           