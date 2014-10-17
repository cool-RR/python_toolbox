# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.caching.cache`.'''


import datetime as datetime_module
import re
import weakref

import nose.tools

from python_toolbox import caching
from python_toolbox.caching import cache
from python_toolbox import misc_tools
from python_toolbox import temp_value_setting
from python_toolbox import cute_testing
from python_toolbox import gc_tools


@misc_tools.set_attributes(i=0)
def counting_func(a=1, b=2, *args, **kwargs):
    '''Function that returns a bigger number every time.'''
    try:
        return counting_func.i
    finally:
        counting_func.i += 1

        
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
    
    class A: pass
    
    a = A()
    result = f(a)
    assert result == f(a) == f(a) == f(a)
    a_ref = weakref.ref(a)    
    del a
    gc_tools.collect()
    assert a_ref() is None
    
    a = A()
    result = f(meow=a)
    assert result == f(meow=a) == f(meow=a) == f(meow=a)
    a_ref = weakref.ref(a)
    del a
    gc_tools.collect()
    
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
    
    x = {1, 2}
    
    assert f(x) == f(x)
    
    assert f(7, x) != f(8, x)
    
    assert f('boo') != f(meow='frrr')
    
    y = {1: [1, 2], 2: frozenset([3, 'b'])}
    
    assert f(meow=y) == f(1, meow=y)
    
    
def test_helpful_message_when_forgetting_parentheses():
    '''Test user gets a helpful exception when when forgetting parentheses.'''

    def confusedly_forget_parentheses():
        @cache
        def f(): pass
        
    with cute_testing.RaiseAssertor(
        TypeError,
        'It seems that you forgot to add parentheses after `@cache` when '
        'decorating the `f` function.'
    ):
        
        confusedly_forget_parentheses()
    
    
    
def test_signature_preservation():
    '''Test that a function's signature is preserved after decorating.'''
    
    f = cache()(counting_func)
    assert f() == f() == f(1, 2) == f(a=1, b=2)
    cute_testing.assert_same_signature(f, counting_func)
    
    def my_func(qq, zz=1, yy=2, *args): pass
    my_func_cached = cache(max_size=7)(my_func)
    cute_testing.assert_same_signature(my_func, my_func_cached)
    
    def my_other_func(**kwargs): pass
    my_func_cached = cache()(my_func)
    cute_testing.assert_same_signature(my_func, my_func_cached)
    
    
def test_api():
    '''Test the API of cached functions.'''
    f = cache()(counting_func)
    g = cache(max_size=3)(counting_func)
    
    for cached_function in (f, g):
    
        assert not hasattr(cached_function, 'cache')
        cute_testing.assert_polite_wrapper(cached_function, counting_func)
        
        result_1 = cached_function(1)
        assert cached_function(1) == result_1 == cached_function(1)
        
        cached_function.cache_clear()
        
        result_2 = cached_function(1)
        
        assert cached_function(1) == result_2 == cached_function(1)
        assert result_1 != result_2 == cached_function(1) != result_1
        
        # Asserting we're not using `dict.clear` or something:
        assert cached_function.cache_clear.__name__ == 'cache_clear'
        
        
def test_double_caching():
    '''Test that `cache` detects and prevents double-caching of functions.'''
    f = cache()(counting_func)
    g = cache()(f)
    
    assert f is g
    
    
def test_time_to_keep():
    counting_func.i = 0 # Resetting so we could refer to hard numbers
                        # without worrying whether other tests made `i` higher.
    f = cache(time_to_keep={'days': 356})(counting_func)
    
    print(f('zero'))
    assert f('zero') == 0 # Just to get rid of zero
    
    assert f('a') == 1
    assert f('b') == 2
    assert f('c') == 3
    assert f('b') == 2
    
    start_datetime = datetime_module.datetime.now()
    fixed_time = start_datetime
    def _mock_now():
        return fixed_time
    
    with temp_value_setting.TempValueSetter(
                                  (caching.decorators, '_get_now'), _mock_now):
        assert list(map(f, 'abc')) == [1, 2, 3]
        fixed_time += datetime_module.timedelta(days=100)
        assert list(map(f, 'abc')) == [1, 2, 3]
        assert list(map(f, 'def')) == [4, 5, 6]
        fixed_time += datetime_module.timedelta(days=100)
        assert list(map(f, 'abc')) == [1, 2, 3]
        assert list(map(f, 'def')) == [4, 5, 6]
        fixed_time += datetime_module.timedelta(days=100)
        assert list(map(f, 'abc')) == [1, 2, 3]
        assert list(map(f, 'def')) == [4, 5, 6]
        fixed_time += datetime_module.timedelta(days=100)
        assert list(map(f, 'abc')) == [7, 8, 9]
        assert list(map(f, 'def')) == [4, 5, 6]
        fixed_time += datetime_module.timedelta(days=100)
        assert list(map(f, 'abc')) == [7, 8, 9]
        assert list(map(f, 'def')) == [10, 11, 12]
        assert f(a='d') == f(a='d', b=2) == f('d') == 10
        fixed_time += datetime_module.timedelta(days=1000)
        assert list(map(f, 'abcdef')) == [13, 14, 15, 16, 17, 18]
        assert f(a='d', b='meow') == 19
        