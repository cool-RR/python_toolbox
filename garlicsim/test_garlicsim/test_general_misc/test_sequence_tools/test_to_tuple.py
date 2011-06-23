# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `sequence_tools.to_tuple`.'''

from __future__ import with_statement

from garlicsim.general_misc import cute_testing

from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc.sequence_tools import to_tuple


def test():
    assert to_tuple((1, 2, 3)) == (1, 2, 3)
    assert to_tuple([1, 2, 3]) == (1, 2, 3)
    assert to_tuple(7) == (7,)
    assert to_tuple((7,)) == (7,)
    assert to_tuple(Ellipsis) == (Ellipsis,)
    
def test_item_type():
    assert to_tuple(7, item_type=int) == (7,)
    assert to_tuple([7], item_type=list) == ([7],)
    assert to_tuple((7,), item_type=tuple) == ((7),)
    
    
def test_item_test():
    
    def is_int_like(item):
        '''Is `item` something like an `int`?'''
        try:
            1 + item
        except Exception:
            return False
        else:
            return True
    
    def is_list_like(item):
        '''Is `item` something like an `int`?''' WAS HERE
        try:
            1 + item
        except Exception:
            return False
        else:
            return True
    
    def is_int_like(item):
        '''Is `item` something like an `int`?'''
        try:
            1 + item
        except Exception:
            return False
        else:
            return True
    
    assert to_tuple(7, item_test=is_int_like) == (7,)
    assert to_tuple([7], item_type=list) == ([7],)
    assert to_tuple((7,), item_type=tuple) == ((7),)
    
    
def test_too_many_arguments():
    
    with cute_testing.RaiseAssertor(text='either'):
        to_tuple(
            (1, 2, 3),
            item_type=int,
            item_test=lambda item: isinstance(item, int)
        )
        