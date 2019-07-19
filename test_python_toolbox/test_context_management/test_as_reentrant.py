# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import generator_stop

import queue as queue_module

from python_toolbox.context_management import (as_reentrant, ContextManager,
                                               ContextManagerType)
from python_toolbox import cute_testing


class MyException(Exception):
    pass


def test_reentrant_context_manager():
    '''Test the basic workings of `ReentrantContextManager`.'''

    class MyContextManager(ContextManager):
        def __init__(self):
            self.times_entered = 0
            self.times_exited = 0
        def __enter__(self):
            self.times_entered += 1
            return self.times_entered
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.times_exited += 1

    get_reentrant_context_manager = lambda: as_reentrant(MyContextManager())

    my_rcm = get_reentrant_context_manager()
    assert my_rcm.__wrapped__.times_entered == 0
    assert my_rcm.__wrapped__.times_exited == 0

    with my_rcm as enter_return_value:
        assert enter_return_value == 1
        assert my_rcm.__wrapped__.times_entered == 1
        assert my_rcm.__wrapped__.times_exited == 0
        with my_rcm as enter_return_value:
            with my_rcm as enter_return_value:
                assert enter_return_value == 1
                assert my_rcm.__wrapped__.times_entered == 1
                assert my_rcm.__wrapped__.times_exited == 0
            assert enter_return_value == 1
            assert my_rcm.__wrapped__.times_entered == 1
            assert my_rcm.__wrapped__.times_exited == 0

    assert my_rcm.__wrapped__.times_entered == 1
    assert my_rcm.__wrapped__.times_exited == 1

    with my_rcm as enter_return_value:
        assert enter_return_value == 2
        assert my_rcm.__wrapped__.times_entered == 2
        assert my_rcm.__wrapped__.times_exited == 1
        with my_rcm as enter_return_value:
            with my_rcm as enter_return_value:
                assert enter_return_value == 2
                assert my_rcm.__wrapped__.times_entered == 2
                assert my_rcm.__wrapped__.times_exited == 1
            assert enter_return_value == 2
            assert my_rcm.__wrapped__.times_entered == 2
            assert my_rcm.__wrapped__.times_exited == 1



    with cute_testing.RaiseAssertor(MyException):
        with my_rcm as enter_return_value:
            assert enter_return_value == 3
            assert my_rcm.__wrapped__.times_entered == 3
            assert my_rcm.__wrapped__.times_exited == 2
            with my_rcm as enter_return_value:
                with my_rcm as enter_return_value:
                    assert enter_return_value == 3
                    assert my_rcm.__wrapped__.times_entered == 3
                    assert my_rcm.__wrapped__.times_exited == 2
                assert enter_return_value == 3
                assert my_rcm.__wrapped__.times_entered == 3
                assert my_rcm.__wrapped__.times_exited == 2
                raise MyException


def test_exception_swallowing():
    class SwallowingContextManager(ContextManager):
        def __init__(self):
            self.times_entered = 0
            self.times_exited = 0
        def __enter__(self):
            self.times_entered += 1
            return self
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.times_exited += 1
            if isinstance(exc_value, MyException):
                return True

    swallowing_rcm = as_reentrant(SwallowingContextManager())

    my_set = set()

    with swallowing_rcm:
        my_set.add(0)
        with swallowing_rcm:
            my_set.add(1)
            with swallowing_rcm:
                my_set.add(2)
                with swallowing_rcm:
                    my_set.add(3)
                    with swallowing_rcm:
                        my_set.add(4)
                        raise MyException
                    my_set.add(5)
                my_set.add(6)
            my_set.add(7)
        my_set.add(8)
    assert my_set == {0, 1, 2, 3, 4}



def test_order_of_depth_modification():
    depth_log = queue_module.Queue()

    class JohnnyContextManager(ContextManager):
        def __enter__(self):
            depth_log.put(johnny_reentrant_context_manager.depth)
            return self
        def __exit__(self, exc_type, exc_value, exc_traceback):
            depth_log.put(johnny_reentrant_context_manager.depth)

    johnny_reentrant_context_manager = as_reentrant(JohnnyContextManager())
    assert johnny_reentrant_context_manager.depth == 0
    with johnny_reentrant_context_manager:
        assert johnny_reentrant_context_manager.depth == 1

        # `.__wrapped__.__enter__` saw a depth of 0, because the depth
        # increment happens *after* `.__wrapped__.__enter__` is called:
        assert depth_log.get(block=False) == 0

        with johnny_reentrant_context_manager:

            assert johnny_reentrant_context_manager.depth == 2
            assert depth_log.qsize() == 0 # We're in a depth greater than 1,
                                          # so `.__wrapped__.__enter__` wasn't
                                          # even called.

        assert johnny_reentrant_context_manager.depth == 1

        assert depth_log.qsize() == 0 # We came out of a depth greater than 1,
                                      # so `.__wrapped__.__enter__` wasn't even
                                      # called.

    # `.__wrapped__.__enter__` saw a depth of 1, because the depth decrement
    # happens *after* `.__wrapped__.__enter__` is called:
    assert depth_log.get(block=False) == 1


def test_decorator_class():

    @as_reentrant
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
            assert meow.n == 1
        assert meow.n == 1
    assert meow.n == 0

def test_decorator_class_enter_exit():

    @as_reentrant
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
            assert meow.n == 1
        assert meow.n == 1
    assert meow.n == 0


def test_decorator_decorator():

    counter = {'n': 0,}

    @as_reentrant
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
            assert counter['n'] == 1
        assert counter['n'] == 1
    assert counter['n'] == 0


