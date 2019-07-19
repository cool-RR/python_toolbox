# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.abc_tools.AbstractStaticMethod`.'''

import sys
import abc

import pytest

from python_toolbox.abc_tools import AbstractStaticMethod


def test_instantiate_without_subclassing():
    '''Test you can't instantiate a class with an `AbstractStaticMethod`.'''

    class A(metaclass=abc.ABCMeta):
        @AbstractStaticMethod
        def f():
            pass

    pytest.raises(TypeError, lambda: A())


def test_override():
    '''
    Can't instantiate subclass that doesn't override `AbstractStaticMethod`.
    '''

    class B(metaclass=abc.ABCMeta):
        @AbstractStaticMethod
        def f():
            pass

    class C(B):
        @staticmethod
        def f():
            return 7

    c = C()

    assert C.f() == c.f() == 7

