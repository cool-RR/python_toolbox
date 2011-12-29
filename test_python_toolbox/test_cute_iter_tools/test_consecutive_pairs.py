# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `cute_iter_tools.consecutive_pairs`.'''

from garlicsim.general_misc import cute_testing
from garlicsim.general_misc import sequence_tools

from garlicsim.general_misc.cute_iter_tools import consecutive_pairs


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
           
           