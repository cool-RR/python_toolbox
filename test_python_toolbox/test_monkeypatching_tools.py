# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.monkeypatching_tools`.'''

from __future__ import with_statement

import uuid

from python_toolbox import cute_testing

from python_toolbox import monkeypatching_tools
from python_toolbox import caching


def test():
    '''Test basic workings of `monkeypatch_method`.'''
    
    class A(object):
        pass

    @monkeypatching_tools.monkeypatch_method(A)
    def meow(a):
        return 1
    
    a = A()
    
    assert a.meow() == meow(a) == 1
    
    @monkeypatching_tools.monkeypatch_method(A, 'roar')
    def woof(a):
        return 2
    
    assert a.roar() == woof(a) == 2
    
    assert not hasattr(a, 'woof')
    
    del meow, woof
    
    
def test_monkeypatch_cached_property():

    class A(object):
        pass

    @monkeypatching_tools.monkeypatch_method(A)
    @caching.CachedProperty
    def meow(a):
        return (type(a), uuid.uuid4().hex)
    
    a0 = A()
    assert a0.meow == a0.meow == a0.meow == a0.meow
    
    a1 = A()
    assert a1.meow == a1.meow == a1.meow == a1.meow
    
    assert a0.meow != a1.meow
    assert a0.meow[0] == a1.meow[0] == A
    
    
    
def test_helpful_message_when_forgetting_parentheses():
    '''Test user gets a helpful exception when when forgetting parentheses.'''

    def confusedly_forget_parentheses():
        @monkeypatching_tools.monkeypatch_method
        def f(): pass
        
    with cute_testing.RaiseAssertor(
        TypeError,
        'It seems that you forgot to add parentheses after '
        '`@monkeypatch_method` when decorating the `f` function.'
    ):
        
        confusedly_forget_parentheses()