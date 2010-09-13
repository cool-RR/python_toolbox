import gc
import weakref

from garlicsim.general_misc.caching import cache


def counting_func(a=1, b=2, *args, **kwargs):
    if not hasattr(counting_func, 'i'):
        counting_func.i = 0
    try:
        return counting_func.i
    finally:
        counting_func.i = (counting_func.i + 1)

        
def test_cache_basic():
    
    my_func = cache(counting_func)
    
    assert my_func() == my_func() == my_func(1, 2) == my_func(a=1, b=2)
    
    assert my_func() != my_func('boo')
    
    assert my_func('boo') == my_func('boo') == my_func(a='boo')
    
    assert my_func('boo') != my_func(meow='frrr')
    
    assert my_func(meow='frrr') == my_func(1, meow='frrr') == my_func(a=1, meow='frrr')
    

def test_cache_weakref():
    
    my_func = cache(counting_func)
    
    class A(object): pass
    
    a = A()
    result = my_func(a)
    assert result == my_func(a) == my_func(a) == my_func(a)
    a_ref = weakref.ref(a)    
    del a
    gc.collect()
    assert a_ref() is None
    
    a = A()
    result = my_func(meow=a)
    assert result == my_func(meow=a) == my_func(meow=a) == my_func(meow=a)
    a_ref = weakref.ref(a)
    del a
    gc.collect()
    assert a_ref() is None
    
    
    
    
    
    