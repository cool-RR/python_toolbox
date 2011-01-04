# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.cute_testing.RaiseAssertor`.'''

import re

import nose

from garlicsim.general_misc.cute_testing import RaiseAssertor


def test_basic():
    with RaiseAssertor(Exception):
        raise Exception
    with RaiseAssertor(TypeError):
        raise Exception
    
    def f():
        with RaiseAssertor(ZeroDivisionError):
            raise Exception
        
    nose.tools.assert_raises(Exception, f)
    
    with RaiseAssertor(Exception) as raise_assertor:
        assert isinstance(raise_assertor, RaiseAssertor)
        with RaiseAssertor(RuntimeError):
            {}[0]
            

def test_decorator():
    
    @RaiseAssertor(ZeroDivisionError)
    def f():
        1/0
        
    f()

    
def test_string():
    
    with RaiseAssertor(Exception, 'wer'):
        raise TypeError('123qwerty456')
    
    with RaiseAssertor(Exception):
        with RaiseAssertor(Exception, 'ooga booga'):
            raise TypeError('123qwerty456')
        
    with RaiseAssertor(Exception):
        with RaiseAssertor(OSError, 'wer'):
            raise SyntaxError('123qwerty456')
        
        
def test_regex():
    with RaiseAssertor(Exception, re.compile('^123\w*?456$')):
        raise TypeError('123qwerty456')
    
    with RaiseAssertor(Exception):
        with RaiseAssertor(Exception, re.compile('^ooga b?ooga$')):
            raise TypeError('123qwerty456')
        
    with RaiseAssertor(Exception):
        with RaiseAssertor(OSError, re.compile('^123\w*?456$')):
            raise SyntaxError('123qwerty456')