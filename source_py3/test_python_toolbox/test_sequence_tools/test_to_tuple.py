# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `sequence_tools.to_tuple`.'''

import nose

from python_toolbox import cute_testing

from python_toolbox import sequence_tools
from python_toolbox.sequence_tools import to_tuple


def test():
    '''Test the basic workings of `sequence_tools.to_tuple`.'''
    assert to_tuple((1, 2, 3)) == (1, 2, 3)
    assert to_tuple([1, 2, 3]) == (1, 2, 3)
    assert to_tuple(7) == (7,)
    assert to_tuple((7,)) == (7,)
    assert to_tuple(Ellipsis) == (Ellipsis,)
    
    
def test_item_type():
    '''Test the `item_type` argument.'''
    assert to_tuple(7, item_type=int) == (7,)
    assert to_tuple([7], item_type=list) == ([7],)
    assert to_tuple([7], item_type=(list, tuple, float)) == ([7],)
    assert to_tuple((7,), item_type=tuple) == ((7,),)
    assert to_tuple((7,), item_type=(tuple, range)) == ((7,),)
    
    
def test_none():
    assert to_tuple(None) == ()
    assert to_tuple(None, item_type=int) == ()
    assert to_tuple(None, item_type=list) == ()
    assert to_tuple(None, item_type=type(None)) == (None,)
    
def test_item_test():    
    '''Test the `item_test` argument.'''
    
    def is_int_like(item):
        '''Is `item` something like an `int`?'''
        try:
            1 + item
        except Exception:
            return False
        else:
            return True
    
    def is_list_like(item):
        '''Is `item` something like a `list`?'''
        try:
            [1, 2] + item
        except Exception:
            return False
        else:
            return True
    
    def is_tuple_like(item):
        '''Is `item` something like an `tuple`?'''
        try:
            (1, 2) + item
        except Exception:
            return False
        else:
            return True
    
    assert to_tuple(7, item_test=is_int_like) == (7,)
    assert to_tuple((1, 2), item_test=is_int_like) == (1, 2)
    assert to_tuple([7], item_test=is_list_like) == ([7],)
    assert to_tuple(([1], [2]), item_test=is_list_like) == ([1], [2])
    assert to_tuple((7,), item_test=is_tuple_like) == ((7,),)

    
def test_tuple_in_tuple():
    '''Test input of tuple inside a tuple.'''
    raise nose.SkipTest("Don't know how to solve this case.")
    assert to_tuple(((1,), (2,)), item_test=is_tuple_like) == ((1,), (2,))
    
    
def test_too_many_arguments():
    '''Test helpful error when giving both `item_type` and `item_test`.'''
    with cute_testing.RaiseAssertor(text='either'):
        to_tuple(
            (1, 2, 3),
            item_type=int,
            item_test=lambda item: isinstance(item, int)
        )
        