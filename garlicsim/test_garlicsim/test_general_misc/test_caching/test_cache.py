# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.caching.cache`.
'''

from __future__ import with_statement

import re
import gc
import weakref

import nose.tools

from garlicsim.general_misc.caching import cache
from garlicsim.general_misc import cute_testing


def counting_func(a=1, b=2, *args, **kwargs):
    '''Function that returns a bigger number every time.'''
    if not hasattr(counting_func, 'i'):
        counting_func.i = 0
    try:
        return counting_func.i
    finally:
        counting_func.i = (counting_func.i + 1)

        
def test_basic():
    '''Test basic workings of `cache`.'''
    f = cache()(counting_func)
    
    assert f() == f() == f(1, 2) == f(a=1, b=2)
    
    assert f() != f('boo')
    
    assert f('boo') == f('boo') == f(a='boo')
    
    assert f('boo') != f(meow='frrr')
    
    assert f(meow='frrr') == f(1, meow='frrr') == f(a=1, meow='frrr')
    

def test_weakref():
    '''Test that `cache` weakrefs weakreffable arguments.'''
    f = cache()(counting_func)
    
    class A(object): pass
    
    a = A()
    result = f(a)
    assert result == f(a) == f(a) == f(a)
    a_ref = weakref.ref(a)    
    del a
    gc.collect()
    assert a_ref() is None
    
    a = A()
    result = f(meow=a)
    assert result == f(meow=a) == f(meow=a) == f(meow=a)
    a_ref = weakref.ref(a)
    del a
    gc.collect()
    
    assert a_ref() is None
    
    
def test_lru():
    '''Test the least-recently-used algorithm for forgetting cached results.'''
    
    f = cache(max_size=3)(counting_func)
    
    r0, r1, r2 = f(0), f(1), f(2)
    
    assert f(0) == f(0) == r0 == f(0)
    assert f(1) == f(1) == r1 == f(1)
    assert f(2) == f(2) == r2 == f(2)
    
    r3 = f(3)
    
    assert f(0) != r0 # Now we recalculated `f(0)` so we forgot `f(1)`
    assert f(2) == f(2) == r2 == f(2)
    assert f(3) == f(3) == r3 == f(3)
    
    new_r1 = f(1)
    
    # Requesting these:
    f(3)
    f(1)
    # So `f(2)` will be the least-recently-used.
    
    r4 = f(4) # Now `f(2)` has been thrown out.
    
    new_r2 = f(2) # And now `f(3)` is thrown out
    assert f(2) != r2
    
    assert f(1) == new_r1 == f(1)
    assert f(4) == r4 == f(4)
    assert f(2) == new_r2 == f(2)
    
    # Now `f(1)` is the least-recently-used.
    
    r5 = f(5) # Now `f(1)` has been thrown out.
    
    assert f(4) == r4 == f(4)
    assert f(5) == r5 == f(5)
    
    assert f(1) != new_r1
    

def test_unhashable_arguments():
    '''Test `cache` works with unhashable arguments.'''
    
    f = cache()(counting_func)
    
    
    assert f(set((1, 2))) == f(set((1, 2)))
    
    assert f(7, set((1, 2))) != f(8, set((1, 2)))
    
    assert f('boo') != f(meow='frrr')
    
    assert f(meow={1: [1, 2], 2: frozenset([3, 'b'])}) == \
           f(1, meow={1: [1, 2], 2: frozenset([3, 'b'])})
    
    
def test_function_instead_of_max_size():
    '''Test user gets a helpful exception when doing `@cache`.'''

    def confusedly_put_function_as_max_size():
        exec('@cache\n'
             'def f():\n'
             '    pass')
        
    with cute_testing.RaiseAssertor(
        TypeError,
        re.compile(
            'You entered the callable `.*?` where you should have '
            'entered the `max_size` for the cache. You probably '
            'used `@cache`, while you should have used `@cache\(\)`'
        )
    ):
        
        confusedly_put_function_as_max_size()
    
    
    
def test_signature_preservation():
    '''Test that a function's signature is preserved after decorating.'''
    
    f = cache()(counting_func)
    assert f() == f() == f(1, 2) == f(a=1, b=2)
    cute_testing.assert_same_signature(f, counting_func)
    
    def my_func(qq, zz=1, yy=2, *args):
        pass
    my_func_cached = cache(max_size=7)(my_func)
    cute_testing.assert_same_signature(my_func, my_func_cached)
    
    def my_other_func(**kwargs):
        pass
    my_func_cached = cache()(my_func)
    cute_testing.assert_same_signature(my_func, my_func_cached)
    
    
    