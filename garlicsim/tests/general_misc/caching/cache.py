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
    
    f = cache()(counting_func)
    
    assert f() == f() == f(1, 2) == f(a=1, b=2)
    
    assert f() != f('boo')
    
    assert f('boo') == f('boo') == f(a='boo')
    
    assert f('boo') != f(meow='frrr')
    
    assert f(meow='frrr') == f(1, meow='frrr') == f(a=1, meow='frrr')
    

def test_cache_weakref():
    
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
    
    
def test_cache_max_size():
    
    f = cache(max_size=3)(counting_func)
    
    r1, r2, r3 = f(1), f(2), f(3)
    
    assert f(1) == f(1) == r1 == f(1)
    assert f(2) == f(2) == r2 == f(2)
    assert f(3) == f(3) == r3 == f(3)
    
    r4 = f(4)
    
    assert f(1) != r1 # Now we recalculated f(1) so we forgot f(2)
    assert f(3) == f(3) == r3 == f(3)
    assert f(4) == f(4) == r4 == f(4)
    
    