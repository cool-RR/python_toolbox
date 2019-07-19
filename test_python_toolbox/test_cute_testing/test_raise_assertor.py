# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.cute_testing.RaiseAssertor`.'''

import re

import pytest

from python_toolbox import cute_testing
from python_toolbox.cute_testing import RaiseAssertor, Failure


class MyException(Exception):
    pass


def test_basic():
    '''Test the basic workings of `RaiseAssertor`.'''
    with RaiseAssertor(Exception):
        raise Exception
    with RaiseAssertor(Exception):
        raise TypeError

    def f():
        with RaiseAssertor(ZeroDivisionError):
            raise MyException
    pytest.raises(Failure, f)
    with RaiseAssertor(Failure):
        f()

    def g():
        with RaiseAssertor(Exception):
            pass
    pytest.raises(Failure, g)
    with RaiseAssertor(Failure):
        g()

    def h():
        with RaiseAssertor(RuntimeError, 'booga'):
            pass
    pytest.raises(Failure, h)
    with RaiseAssertor(Failure):
        h()

    with RaiseAssertor(Failure) as raise_assertor:
        assert isinstance(raise_assertor, RaiseAssertor)
        with RaiseAssertor(RuntimeError):
            {}[0]

    assert isinstance(raise_assertor.exception, Exception)


def test_decorator():
    '''Test using `RaiseAssertor` as a decorator.'''
    @RaiseAssertor(ZeroDivisionError)
    def f():
        1/0

    f()

    cute_testing.assert_polite_wrapper(f)


def test_string():
    '''
    Test using `RaiseAssertor` specifying sub-string of the exception message.
    '''
    with RaiseAssertor(Exception, 'wer'):
        raise TypeError('123qwerty456')

    with RaiseAssertor(Failure):
        with RaiseAssertor(Exception, 'ooga booga'):
            raise TypeError('123qwerty456')

    with RaiseAssertor(Failure):
        with RaiseAssertor(OSError, 'wer'):
            raise SyntaxError('123qwerty456')


def test_regex():
    '''
    Test using `RaiseAssertor` specifying regex pattern for exception message.
    '''
    with RaiseAssertor(Exception, re.compile(r'^123\w*?456$')):
        raise TypeError('123qwerty456')

    with RaiseAssertor(Failure):
        with RaiseAssertor(Exception, re.compile('^ooga b?ooga$')):
            raise TypeError('123qwerty456')

    with RaiseAssertor(Failure):
        with RaiseAssertor(OSError, re.compile(r'^123\w*?456$')):
            raise SyntaxError('123qwerty456')


def test_assert_exact_type():
    '''Test `RaiseAssertor`'s `assert_exact_type` option.'''
    with RaiseAssertor(LookupError):
        raise KeyError("Look at me, I'm a KeyError")

    error_message = (
        "was raised, and it *is* an instance of the LookupError we were "
        "expecting; but its type is not LookupError, it's KeyError, which "
        "is a subclass of LookupError, and you specified "
        "`assert_exact_type=True`, so subclasses aren't acceptable."
    )

    with RaiseAssertor(Failure, error_message):
        with RaiseAssertor(LookupError, assert_exact_type=True):
            raise KeyError("Look at me, I'm a KeyError")



