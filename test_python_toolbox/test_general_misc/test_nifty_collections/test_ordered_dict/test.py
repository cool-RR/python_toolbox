# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `nifty_collections.ordered_dict.OrderedDict`.'''

from __future__ import with_statement

from garlicsim.general_misc import cute_testing

from garlicsim.general_misc.nifty_collections.ordered_dict import OrderedDict


def test_sort():
    '''Test the `OrderedDict.sort` method.'''
    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    ordered_dict_copy = ordered_dict.copy()
    assert ordered_dict == ordered_dict_copy
    ordered_dict.sort()
    assert ordered_dict == ordered_dict_copy
        
    ordered_dict_copy.sort(key=(lambda x: -x))
    assert ordered_dict != ordered_dict_copy
    assert ordered_dict == dict(ordered_dict) == ordered_dict_copy
    
    ordered_dict[4] = ordered_dict_copy[4] = 'd'
    assert ordered_dict != ordered_dict_copy
    assert ordered_dict == dict(ordered_dict) == ordered_dict_copy
    
    ordered_dict_copy.sort(key=ordered_dict_copy.__getitem__)
    assert ordered_dict == ordered_dict_copy
    
    ordered_dict_copy.sort(key=(lambda x: -x))
    assert ordered_dict != ordered_dict_copy
    assert ordered_dict == dict(ordered_dict) == ordered_dict_copy
    
    ordered_dict.sort(key=(lambda x: -x))
    assert ordered_dict == ordered_dict_copy
    
    
def test_index():
    '''Test the `OrderedDict.index` method.'''
    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    assert ordered_dict.index(1) == 0
    assert ordered_dict.index(3) == 2
    assert ordered_dict.index(2) == 1
    
    ordered_dict[2] = 'b'
    
    assert ordered_dict.index(1) == 0
    assert ordered_dict.index(3) == 2
    assert ordered_dict.index(2) == 1
    
    ordered_dict['meow'] = 'frr'
    
    assert ordered_dict.index('meow') == 3
    
    with cute_testing.RaiseAssertor(KeyError):
        ordered_dict.index('Non-existing key')