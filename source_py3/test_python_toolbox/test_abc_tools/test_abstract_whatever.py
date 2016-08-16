# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import sys
import abc

import nose

from python_toolbox import cute_testing

from python_toolbox.abc_tools import abstract_whatever


def test():
    
    class A(metaclass=abc.ABCMeta):
        foo = abstract_whatever()
        
        @abstract_whatever
        def bar(self): pass
        
    with cute_testing.RaiseAssertor(TypeError):
        A()
    

    class B(A):
        pass
    
    with cute_testing.RaiseAssertor(TypeError):
        B()
    
    
    class C(A):
        foo = 7
    
    with cute_testing.RaiseAssertor(TypeError):
        C()
    
    
    class D(A):
        foo = 7
        bar = 9
    
    D()
    

    class E(A):
        def foo(self): pass
        def bar(self): pass
    
    E()
    
    
            
            
            
    