# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.cute_testing.RaiseAssertor`.'''

from __future__ import with_statement

import re

import nose

from garlicsim.general_misc.cute_testing import RaiseAssertor, Failure


class MyException(Exception):
    pass


def test_basic():
    with RaiseAssertor(Exception):
        raise Exception
    with RaiseAssertor(Exception):
        raise TypeError
    
    def f():
        with RaiseAssertor(ZeroDivisionError):
            raise MyException
    nose.tools.assert_raises(MyException, f)
    with RaiseAssertor(MyException):
        f()
    
    def g():
        with RaiseAssertor(Exception):
            pass
    nose.tools.assert_raises(Failure, g)
    with RaiseAssertor(Failure):
        g()
    
    def h():
        with RaiseAssertor(RuntimeError, 'booga'):
            pass
    nose.tools.assert_raises(Failure, h)
    with RaiseAssertor(Failure):
        h()
    
    with RaiseAssertor(Exception) as raise_assertor:
        assert isinstance(raise_assertor, RaiseAssertor)
        with RaiseAssertor(RuntimeError):
            {}[0]
            
    assert isinstance(raise_assertor.exception, Exception)
            

def test_decorator():
    
    @RaiseAssertor(ZeroDivisionError)
    def f():
        1/0
        
    f()

    
def test_string():
    
    with RaiseAssertor(Exception, 'wer'):
        raise TypeError('123qwerty456')
    
    with RaiseAssertor(Failure):
        with RaiseAssertor(Exception, 'ooga booga'):
            raise TypeError('123qwerty456')
        
    with RaiseAssertor(Failure):
        with RaiseAssertor(OSError, 'wer'):
            raise SyntaxError('123qwerty456')
        
        
def test_regex():
    with RaiseAssertor(Exception, re.compile('^123\w*?456$')):
        raise TypeError('123qwerty456')
    
    with RaiseAssertor(Failure):
        with RaiseAssertor(Exception, re.compile('^ooga b?ooga$')):
            raise TypeError('123qwerty456')
        
    with RaiseAssertor(Failure):
        with RaiseAssertor(OSError, re.compile('^123\w*?456$')):
            raise SyntaxError('123qwerty456')