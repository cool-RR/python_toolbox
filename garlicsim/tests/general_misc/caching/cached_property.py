import nose

from garlicsim.general_misc.caching import (cache, CachedType,
                                            CachedProperty)


def counting_func(self):
    if not hasattr(counting_func, 'i'):
        counting_func.i = 0
    try:
        return counting_func.i
    finally:
        counting_func.i = (counting_func.i + 1)
    
        
def test_cached_property():
        
    class A(object):
        personality = CachedProperty(counting_func)
    
    assert isinstance(A.personality, CachedProperty)
        
    a = A()
    assert a.personality == a.personality == a.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a.personality + 1        


def test_cached_property_as_decorator():
        
    class B(object):
        @CachedProperty
        def personality(self):
            if not hasattr(counting_func, 'i'):
                counting_func.i = 0
            try:
                return counting_func.i
            finally:
                counting_func.i = (counting_func.i + 1) % 10
    
    assert isinstance(B.personality, CachedProperty)                
                
    b = B()
    assert b.personality == b.personality == b.personality
    
    b2 = B()
    assert b2.personality == b2.personality == b2.personality 
    
    assert b2.personality == b.personality + 1
        
    
def test_cached_property_with_name():
        
    class A(object):
        personality = CachedProperty(counting_func, name='personality')
    
    a = A()
    assert a.personality == a.personality == a.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a.personality + 1
        
    
def test_cached_property_with_wrong_name():
        
    class A(object):
        personality = CachedProperty(counting_func, name='meow')
    
    a = A()
    assert a.personality == a.meow == a.personality - 1 == a.personality - 2
    
    a2 = A()
    assert a2.personality == a2.meow == a2.personality - 1 == a2.personality - 2
    
    