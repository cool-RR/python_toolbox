# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `logic_tools.all_equal`.'''

import operator
import itertools

from python_toolbox.logic_tools import all_equivalent


def test():
    '''Test the basic working of `all_equal`.'''
    _check(False)
    _check(True)


def _check(exhaustive):
    '''Check the basic working of `all_equal` with given `exhaustive` flag.'''
    assert all_equivalent([1, 1, 1, 1], exhaustive=exhaustive)
    assert all_equivalent([1, 1, 1.0, 1], exhaustive=exhaustive)
    assert all_equivalent(((1 + 0j), 1, 1.0, 1), exhaustive=exhaustive)
    assert all_equivalent([], exhaustive=exhaustive)
    assert all_equivalent(iter([1, 1, 1.0, 1]), exhaustive=exhaustive)
    assert all_equivalent({'meow'}, exhaustive=exhaustive)
    assert all_equivalent(['frr', 'frr', 'frr', 'frr'], exhaustive=exhaustive)
    
    assert not all_equivalent([1, 1, 2, 1], exhaustive=exhaustive)
    assert not all_equivalent([1, 1, 1.001, 1], exhaustive=exhaustive)
    assert not all_equivalent(((1 + 0j), 3, 1.0, 1), exhaustive=exhaustive)
    assert not all_equivalent(range(7), exhaustive=exhaustive)
    assert not all_equivalent(iter([1, 17, 1.0, 1]), exhaustive=exhaustive)
    assert not all_equivalent({'meow', 'grr'}, exhaustive=exhaustive)
    assert not all_equivalent(['frr', 'frr', {}, 'frr', 'frr'],
                              exhaustive=exhaustive)
    assert not all_equivalent(itertools.count()) # Not using given `exhaustive`
                                            # flag here because `count()` is
                                            # infinite.
    
    
def test_exhaustive_true():
    '''Test `all_equal` in cases where `exhaustive=True` is relevant.'''
    
    class FunkyFloat(float):
        def __eq__(self, other):
            return (abs(self - other) <= 2)
        
    funky_floats = [
        FunkyFloat(1),
        FunkyFloat(2),
        FunkyFloat(3),
        FunkyFloat(4)
    ]
    
    assert all_equivalent(funky_floats)
    assert not all_equivalent(funky_floats, exhaustive=True)
                
    
    
def test_custom_relations():
    assert all_equivalent(range(4), relation=operator.ne) is True
    assert all_equivalent(range(4), relation=operator.ge) is False
    assert all_equivalent(range(4), relation=operator.le) is True
    assert all_equivalent(range(4), relation=operator.le,
                          exhaustive=True) is True
    # (Always comparing small to big, even on exhaustive.)
    
    assert all_equivalent(range(4),
                          relation=lambda x, y: (x // 10 == y // 10)) is True
    assert all_equivalent(range(4),
                          relation=lambda x, y: (x // 10 == y // 10),
                          exhaustive=True) is True
    assert all_equivalent(range(8, 12), 
                          relation=lambda x, y: (x // 10 == y // 10)) is False
    assert all_equivalent(range(8, 12),
                          relation=lambda x, y: (x // 10 == y // 10),
                          exhaustive=True) is False
    