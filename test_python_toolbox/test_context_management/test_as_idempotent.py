# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import generator_stop

import queue as queue_module

from python_toolbox.context_management import (as_idempotent, ContextManager,
                                               ContextManagerType)
from python_toolbox import cute_testing


class SomeContextManager(ContextManager):
    x = 0
    def manage_context(self):
        self.x += 1
        try:
            yield (self, self)
        except ZeroDivisionError:
            pass
        finally:
            self.x -= 1



def test_as_idempotent():
    some_context_manager = SomeContextManager()
    assert some_context_manager.x == 0
    with some_context_manager as enter_result:
        assert isinstance(enter_result, tuple)
        assert len(enter_result) == 2
        assert enter_result[0] is enter_result[1] is some_context_manager
        assert some_context_manager.x == 1
    assert some_context_manager.x == 0

    some_context_manager.__enter__()
    assert some_context_manager.x == 1
    some_context_manager.__enter__()
    assert some_context_manager.x == 2
    some_context_manager.__enter__()
    assert some_context_manager.x == 3
    some_context_manager.__exit__(None, None, None)
    assert some_context_manager.x == 2
    some_context_manager.__exit__(None, None, None)
    assert some_context_manager.x == 1
    some_context_manager.__exit__(None, None, None)
    assert some_context_manager.x == 0
    with cute_testing.RaiseAssertor():
        some_context_manager.__exit__(None, None, None)
    with cute_testing.RaiseAssertor():
        some_context_manager.__exit__(None, None, None)

    with cute_testing.RaiseAssertor(KeyError):
        with some_context_manager:
            raise KeyError

    with some_context_manager:
        raise ZeroDivisionError

    ###########################################################################


    another_context_manager = SomeContextManager()
    idempotent_context_manager = as_idempotent(another_context_manager)

    assert another_context_manager is idempotent_context_manager.__wrapped__

    with idempotent_context_manager as enter_result:
        assert isinstance(enter_result, tuple)
        assert len(enter_result) == 2
        assert enter_result[0] is enter_result[1] is another_context_manager
        assert another_context_manager.x == 1


    idempotent_context_manager.__enter__()
    assert idempotent_context_manager.__wrapped__.x == 1
    idempotent_context_manager.__enter__()
    assert idempotent_context_manager.__wrapped__.x == 1
    idempotent_context_manager.__enter__()
    assert idempotent_context_manager.__wrapped__.x == 1
    idempotent_context_manager.__exit__(None, None, None)
    assert idempotent_context_manager.__wrapped__.x == 0
    idempotent_context_manager.__exit__()
    assert idempotent_context_manager.__wrapped__.x == 0
    idempotent_context_manager.__exit__(None, None, None)
    assert idempotent_context_manager.__wrapped__.x == 0

    with cute_testing.RaiseAssertor(KeyError):
        with idempotent_context_manager:
            raise KeyError

    with idempotent_context_manager:
        raise ZeroDivisionError


def test_decorator_class():

    @as_idempotent
    class Meow(ContextManager):
        n = 0

        def manage_context(self):
            self.n += 1
            try:
                yield
            finally:
                self.n -= 1


    meow = Meow()
    assert meow.n == 0
    with meow:
        assert meow.n == 1
        with meow:
            assert meow.n == 1
            with meow:
                assert meow.n == 1
            assert meow.n == 0
        assert meow.n == 0
    assert meow.n == 0

def test_decorator_class_enter_exit():

    @as_idempotent
    class Meow(ContextManager):
        n = 0

        def __enter__(self):
            self.n += 1
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.n -= 1


    meow = Meow()
    assert meow.n == 0
    with meow:
        assert meow.n == 1
        with meow:
            assert meow.n == 1
            with meow:
                assert meow.n == 1
            assert meow.n == 0
        assert meow.n == 0
    assert meow.n == 0


def test_decorator_decorator():

    counter = {'n': 0,}

    @as_idempotent
    @ContextManagerType
    def Meow():
        counter['n'] += 1
        try:
            yield
        finally:
            counter['n'] -= 1


    meow = Meow()
    assert counter['n'] == 0
    with meow:
        assert counter['n'] == 1
        with meow:
            assert counter['n'] == 1
            with meow:
                assert counter['n'] == 1
            assert counter['n'] == 0
        assert counter['n'] == 0
    assert counter['n'] == 0


