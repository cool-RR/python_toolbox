# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Test package for `dict_tools.reverse_with_set_values`.'''

from python_toolbox import dict_tools
from python_toolbox import nifty_collections


def test():
    '''Test the basic workings of `reverse_with_set_values`.'''
    assert dict_tools.reverse_with_set_values({1: 2, 3: 4, 'meow': 2}) == \
                                             {2: set([1, 'meow']), 4: set([3])}
    
def test_iterable_input():
    assert dict_tools.reverse_with_set_values((list(range(1, 5)), str)) == \
        {'1': set([1]), '2': set([2]), '3': set([3]), '4': set([4]),}
    
    assert dict_tools.reverse_with_set_values(([1, 2+3j, 4, 5-6j], 'imag')) \
                           == {0: set([1, 4]), 3: set([2+3j]), -6: set([5-6j])}
    
    
def test_ordered_dict_output():
    assert dict_tools.reverse_with_set_values({1: 2, 3: 4, 'meow': 2},
                                              sort=True) == \
    nifty_collections.OrderedDict([(2, set([1, 'meow'])), (4, set([3]))])
    
    assert dict_tools.reverse_with_set_values({1: 2, 3: 4, 'meow': 2},
                                              sort=lambda x: -x) == \
    nifty_collections.OrderedDict([(4, set([3])), (2, set([1, 'meow']))])
    