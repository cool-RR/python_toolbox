
from garlicsim.general_misc.caching import (cache, CachedType,
                                            LazilyEvaluatedConstantProperty)

def rotating_func(self):
    if not hasattr(rotating_func, 'i'):
        rotating_func.i = 0
    try:
        return rotating_func.i
    finally:
        rotating_func.i = (rotating_func.i + 1) % 10
    
        
def test_lec_property():
        
    class A(object):
        personality = LazilyEvaluatedConstantProperty(rotating_func)
    
    a = A()
    assert a.personality == a.personality == a.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a.personality + 1
        
    
def test_lec_property_with_name():
        
    class A(object):
        personality = LazilyEvaluatedConstantProperty(rotating_func,
                                                      name='personality')
    
    a = A()
    assert a.personality == a.personality == a.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a.personality + 1
        
    
def test_lec_property_with_wrong_name():
        
    class A(object):
        personality = LazilyEvaluatedConstantProperty(rotating_func,
                                                      name='meow')
    
    a = A()
    assert a.personality == a.meow == a.personality - 1 == a.personality - 2
    
    a2 = A()
    assert a2.personality == a2.meow == a2.personality - 1 == a2.personality - 2
    
    