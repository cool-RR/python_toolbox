# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.


import sys
import uuid
import types

import nose

from python_toolbox import cute_inspect
from python_toolbox import cute_testing

from python_toolbox import monkeypatching_tools
from python_toolbox import caching


class EqualByIdentity:
    def __eq__(self, other):
        return self is other


def test():
    '''Test basic workings of `monkeypatch`.'''
    
    class A(EqualByIdentity):
        pass

    @monkeypatching_tools.monkeypatch(A)
    def meow(a):
        return (a, 1)
    
    a = A()
    
    assert a.meow() == meow(a) == (a, 1)
    
    @monkeypatching_tools.monkeypatch(A, 'roar')
    def woof(a):
        return (a, 2)
    
    assert a.roar() == woof(a) == (a, 2)
    
    assert not hasattr(a, 'woof')
    
    del meow, woof
    
    
def test_without_override():
    
    class A(EqualByIdentity):
        def booga(self):
            return 'Old method'

    @monkeypatching_tools.monkeypatch(A, override_if_exists=False)
    def meow(a):
        return (a, 1)
    
    a = A()
    
    assert a.meow() == meow(a) == (a, 1)
    
    
    @monkeypatching_tools.monkeypatch(A, override_if_exists=False)
    def booga():
        raise RuntimeError('Should never be called.')
    
    a = A()
    
    assert a.booga() == 'Old method'
    
    
    
def test_monkeypatch_property():

    class A(EqualByIdentity):
        pass

    @monkeypatching_tools.monkeypatch(A)
    @property
    def meow(a):
        return (type(a), 'bark')
    
    a0 = A()
    a1 = A()
    assert a0.meow == a1.meow == (A, 'bark') 
    
    
def test_monkeypatch_cached_property():

    class A(EqualByIdentity):
        pass

    @monkeypatching_tools.monkeypatch(A)
    @caching.CachedProperty
    def meow(a):
        return (type(a), uuid.uuid4().hex)
    
    a0 = A()
    assert a0.meow == a0.meow == a0.meow == a0.meow
    
    a1 = A()
    assert a1.meow == a1.meow == a1.meow == a1.meow
    
    assert a0.meow != a1.meow
    assert a0.meow[0] == a1.meow[0] == A
    
    
def test_monkeypatch_lambda_property():

    class A(EqualByIdentity):
        pass

    monkeypatching_tools.monkeypatch(A, 'meow')(
        property(lambda self: (type(self), 'bark'))
    )
    
    a0 = A()
    a1 = A()
    assert a0.meow == a1.meow == (A, 'bark') 
    
    
def test_helpful_message_when_forgetting_parentheses():
    '''Test user gets a helpful exception when when forgetting parentheses.'''

    def confusedly_forget_parentheses():
        @monkeypatching_tools.monkeypatch
        def f(): pass
        
    with cute_testing.RaiseAssertor(
        TypeError,
        'It seems that you forgot to add parentheses after '
        '`@monkeypatch` when decorating the `f` function.'
    ):
        
        confusedly_forget_parentheses()
        

def test_monkeypatch_staticmethod():

    class A(EqualByIdentity):
        @staticmethod
        def my_static_method(x):
            raise 'Flow should never reach here.'
        
    @monkeypatching_tools.monkeypatch(A)
    @staticmethod
    def my_static_method(x):
        return (x, 'Success')
    
    assert isinstance(cute_inspect.getattr_static(A, 'my_static_method'),
                      staticmethod)
    assert isinstance(A.my_static_method, types.FunctionType)
    
    assert A.my_static_method(3) == A.my_static_method(3) == (3, 'Success')
    
    a0 = A()
    assert a0.my_static_method(3) == a0.my_static_method(3) == (3, 'Success')
    
    
def test_monkeypatch_classmethod():

    class A(EqualByIdentity):
        @classmethod
        def my_class_method(cls):
            raise 'Flow should never reach here.'
        
    @monkeypatching_tools.monkeypatch(A)
    @classmethod
    def my_class_method(cls):
        return cls

    assert isinstance(cute_inspect.getattr_static(A, 'my_class_method'),
                      classmethod)
    assert isinstance(A.my_class_method, types.MethodType)
    
    assert A.my_class_method() == A
    
    a0 = A()
    assert a0.my_class_method() == A
        
        
        
def test_monkeypatch_classmethod_subclass():
    '''
    Test `monkeypatch` on a subclass of `classmethod`.
    
    This is useful in Django, that uses its own `classmethod` subclass.
    '''
    class FunkyClassMethod(classmethod):
        is_funky = True

    class A(EqualByIdentity):
        @FunkyClassMethod
        def my_funky_class_method(cls):
            raise 'Flow should never reach here.'
        
    @monkeypatching_tools.monkeypatch(A)
    @FunkyClassMethod
    def my_funky_class_method(cls):
        return cls

    assert isinstance(cute_inspect.getattr_static(A, 'my_funky_class_method'),
                      FunkyClassMethod)
    assert cute_inspect.getattr_static(A, 'my_funky_class_method').is_funky
    assert isinstance(A.my_funky_class_method, types.MethodType)
    
    assert A.my_funky_class_method() == A
    
    a0 = A()
    assert a0.my_funky_class_method() == A
        

def test_directly_on_object():
    
    class A(EqualByIdentity):
        def woof(self):
            return (self, 'woof')

    a0 = A()
    a1 = A()

    @monkeypatching_tools.monkeypatch(a0)
    def meow(a):
        return 'not meow'
    
    @monkeypatching_tools.monkeypatch(a0)
    def woof(a):
        return 'not woof'
    
    assert a0.meow() == 'not meow'
    assert a0.woof() == 'not woof'
    
    assert a1.woof() == (a1, 'woof')
    
    with cute_testing.RaiseAssertor(AttributeError):
        A.meow()
    with cute_testing.RaiseAssertor(AttributeError):
        a1.meow()
        
    assert A.woof(a0) == (a0, 'woof')
    

def test_monkeypatch_module():
    module = types.ModuleType('module')
    assert not hasattr(module, 'meow')
    @monkeypatching_tools.monkeypatch(module)
    def meow():
        return 'First meow'
    assert module.meow() == 'First meow'
    
    @monkeypatching_tools.monkeypatch(module, override_if_exists=False)
    def meow():
        return 'Second meow'
    assert module.meow() == 'First meow'
    
    @monkeypatching_tools.monkeypatch(module, name='woof', override_if_exists=False)
    def meow():
        return 'Third meow'
    assert module.woof() == 'Third meow'