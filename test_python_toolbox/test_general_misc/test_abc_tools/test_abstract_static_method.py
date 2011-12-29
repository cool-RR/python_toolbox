# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.abc_tools.AbstractStaticMethod`.
'''

import sys

import nose

from garlicsim.general_misc.abc_tools import AbstractStaticMethod
from garlicsim.general_misc.third_party import abc


def test_instantiate_without_subclassing():
    '''Test you can't instantiate a class with an `AbstractStaticMethod`.'''
    
    if sys.version_info[:2] <= (2, 5):
        raise nose.SkipTest("Python 2.5 and below can't enforce abstract "
                            "methods.")
    
    class A(object):
        __metaclass__ = abc.ABCMeta
        
        @AbstractStaticMethod
        def f():
            pass
         
    nose.tools.assert_raises(TypeError, lambda: A())
    
        
def test_override():
    '''
    Can't instantiate subclass that doesn't override `AbstractStaticMethod`.
    '''
    
    class B(object):
        __metaclass__ = abc.ABCMeta
        
        @AbstractStaticMethod
        def f():
            pass
    
    class C(B):
        @staticmethod
        def f():
            return 7
        
    c = C()
    
    assert C.f() == c.f() == 7
    
    