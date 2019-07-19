# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Module for testing the abstract methods of `ContextManager`.'''

from __future__ import generator_stop

import sys

import pytest

from python_toolbox.context_management import (
    ContextManager, ContextManagerType, SelfHook, AbstractContextManager
)

def test_abstractness():
    '''
    A non-abstract-overriding `ContextManager` subclass can't be instantiated.
    '''

    class EmptyContextManager(ContextManager):
        pass

    class EnterlessContextManager(ContextManager):
        def __exit__(self, exc_type, exc_value, exc_traceback):
            pass

    class ExitlessContextManager(ContextManager):
        def __enter__(self):
            pass

    def f():
        EmptyContextManager()

    def g():
        EnterlessContextManager()

    def h():
        ExitlessContextManager()

    pytest.raises(TypeError, f)
    pytest.raises(TypeError, g)
    pytest.raises(TypeError, h)


def test_can_instantiate_when_defining_manage_context():
    '''
    A `manage_context`-defining `ContextManager` subclass can be instantiated.
    '''
    class MyContextManager(ContextManager):
        def manage_context(self):
            yield self
    MyContextManager()


def test_can_instantiate_when_defining_enter_exit():
    '''
    An enter/exit -defining `ContextManager` subclass can be instantiated.
    '''
    class AnotherContextManager(ContextManager):
        def __enter__(self):
            pass
        def __exit__(self, exc_type, exc_value, exc_traceback):
            pass
    AnotherContextManager()

def test_isinstance_and_issubclass():
    class Woof:
        def __enter__(self):
            return self
    class Meow:
        def __exit__(self, exc_type, exc_value, exc_traceback):
            return False
    class Good(Woof, Meow):
        pass

    assert not issubclass(object, AbstractContextManager)
    assert not issubclass(Woof, AbstractContextManager)
    assert not issubclass(Meow, AbstractContextManager)
    assert issubclass(Good, AbstractContextManager)

    assert not isinstance(object(), AbstractContextManager)
    assert not isinstance(Woof(), AbstractContextManager)
    assert not isinstance(Meow(), AbstractContextManager)
    assert isinstance(Good(), AbstractContextManager)





