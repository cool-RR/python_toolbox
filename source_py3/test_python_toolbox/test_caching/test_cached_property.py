# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.caching.CachedProperty`.'''

import nose

from python_toolbox import context_management
from python_toolbox import misc_tools

from python_toolbox.caching import cache, CachedType, CachedProperty


@misc_tools.set_attributes(i=0)
def counting_func(self):
    '''Return a bigger number every time.'''
    try:
        return counting_func.i
    finally:
        counting_func.i += 1
    
        
def test():
    '''Test basic workings of `CachedProperty`.'''    
    class A:
        personality = CachedProperty(counting_func)
    
    assert isinstance(A.personality, CachedProperty)
        
    a1 = A()
    assert a1.personality == a1.personality == a1.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a1.personality + 1

def test_inheritance():
    class A:
        personality = CachedProperty(counting_func)
    
    class B(A):
        pass
    
    assert isinstance(B.personality, CachedProperty)
        
    b1 = B()
    assert b1.personality == b1.personality == b1.personality
    
    b2 = B()
    assert b2.personality == b2.personality == b2.personality 
    
    assert b2.personality == b1.personality + 1

def test_value():
    '''Test `CachedProperty` when giving a value instead of a getter.'''
    class B:
        brrr_property = CachedProperty('brrr')
    
    assert isinstance(B.brrr_property, CachedProperty)
        
    b1 = B()
    assert b1.brrr_property == 'brrr'
    
    b2 = B()
    assert b2.brrr_property == 'brrr'


def test_as_decorator():
    '''Test `CachedProperty` can work as a decorator.'''
    class B:
        @CachedProperty
        def personality(self):
            if not hasattr(B.personality, 'i'):
                B.personality.i = 0
            try:
                return B.personality.i
            finally:
                B.personality.i = (B.personality.i + 1)
    
    assert isinstance(B.personality, CachedProperty)                
                
    b1 = B()
    assert b1.personality == b1.personality == b1.personality

    
    b2 = B()
    assert b2.personality == b2.personality == b2.personality 
    
    assert b2.personality == b1.personality + 1
        
    
def test_with_name():
    '''Test `CachedProperty` works with correct name argument.'''
    class A:
        personality = CachedProperty(counting_func, name='personality')
    
    a1 = A()
    assert a1.personality == a1.personality == a1.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a1.personality + 1
        
    
def test_with_wrong_name():
    '''Test `CachedProperty`'s behavior with wrong name argument.'''
        
    class A:
        personality = CachedProperty(counting_func, name='meow')
    
    a1 = A()
    assert a1.personality == a1.meow == a1.personality - 1 == \
           a1.personality - 2
    
    a2 = A()
    assert a2.personality == a2.meow == a2.personality - 1 == \
           a2.personality - 2
    
    
def test_on_false_object():
    '''Test `CachedProperty` on class that evaluates to `False`.'''
    
    class C:
        @CachedProperty
        def personality(self):
            if not hasattr(C.personality, 'i'):
                C.personality.i = 0
            try:
                return C.personality.i
            finally:
                C.personality.i = (C.personality.i + 1)
        
        def __bool__(self):
            return False
        
        __nonzero__ = __bool__
        
    assert isinstance(C.personality, CachedProperty)
                
    c1 = C()
    assert not c1
    assert c1.personality == c1.personality == c1.personality
    
    c2 = C()
    assert not c2
    assert c2.personality == c2.personality == c2.personality 
    
    assert c2.personality == c1.personality + 1
    
    
def test_doc():
    '''Test the `doc` argument for setting the property's docstring.'''
    class A:
        personality = CachedProperty(counting_func)
        
    assert A.personality.__doc__ ==  'Return a bigger number every time.'
    
    
    class B:
        personality = CachedProperty(
            counting_func,
            doc='''Ooga booga.'''
        )
        
    assert B.personality.__doc__ ==  'Ooga booga.'
    
    
    class C:
        undocced_property = CachedProperty(
            lambda self: 1/0,
        )
        
    assert C.undocced_property.__doc__ is None

    
def test_decorating():
    '''Test method-decorating functionality.'''
    
    class A:
        reentrant_context_manager = CachedProperty(
            lambda self: context_management.ReentrantContextManager()
        )
        
        @reentrant_context_manager
        def my_method(self, x, y=3):
            return (x, y, self.reentrant_context_manager.depth)
        
    a = A()
    
    assert a.my_method(2) == (2, 3, 1)
    with a.reentrant_context_manager:
        assert a.my_method(y=7, x=8) == (8, 7, 2)
        with a.reentrant_context_manager:
            assert a.my_method(y=7, x=8) == (8, 7, 3)
        
def test_force_value_not_getter():
    class A:
        personality = CachedProperty(counting_func,
                                     force_value_not_getter=True)
        
    a = A()
    assert a.personality == counting_func == a.personality == counting_func
    