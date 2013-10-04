# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `logic_tools.all_equal`.'''

import itertools

from python_toolbox.logic_tools import all_equal


def test():
    '''Test the basic working of `all_equal`.'''
    yield _check, False
    yield _check, True


def _check(exhaustive):
    '''Check the basic working of `all_equal` with given `exhaustive` flag.'''
    assert all_equal([1, 1, 1, 1], exhaustive)
    assert all_equal([1, 1, 1.0, 1], exhaustive)
    assert all_equal(((1 + 0j), 1, 1.0, 1), exhaustive)
    assert all_equal([], exhaustive)
    assert all_equal(iter([1, 1, 1.0, 1]), exhaustive)
    assert all_equal({'meow'}, exhaustive)
    assert all_equal(['frr', 'frr', 'frr', 'frr'], exhaustive)
    
    assert not all_equal([1, 1, 2, 1], exhaustive)
    assert not all_equal([1, 1, 1.001, 1], exhaustive)
    assert not all_equal(((1 + 0j), 3, 1.0, 1), exhaustive)
    assert not all_equal(range(7), exhaustive)
    assert not all_equal(iter([1, 17, 1.0, 1]), exhaustive)
    assert not all_equal({'meow', 'grr'}, exhaustive)
    assert not all_equal(['frr', 'frr', {}, 'frr', 'frr'], exhaustive)
    assert not all_equal(itertools.count()) # Not using given `exhaustive`
                                            # flag here because `count()` is
                                            # infinite.
    
    
def test_exhaustive():
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
    
    assert all_equal(funky_floats)
    assert not all_equal(funky_floats, exhaustive=True)
                
