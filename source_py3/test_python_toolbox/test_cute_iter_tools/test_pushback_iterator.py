# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.cute_iter_tools import PushbackIterator


def test_pushback_iterator():
    
    pushback_iterator = PushbackIterator(iter([1, 2, 3]))
    assert next(pushback_iterator) == 1
    assert next(pushback_iterator) == 2
    pushback_iterator.push_back()
    assert next(pushback_iterator) == 2
    assert next(pushback_iterator) == 3
    pushback_iterator.push_back()
    assert next(pushback_iterator) == 3
    with cute_testing.RaiseAssertor(StopIteration):
        next(pushback_iterator)
    pushback_iterator.push_back()
    assert next(pushback_iterator) == 3
    
    with cute_testing.RaiseAssertor(StopIteration):
        next(pushback_iterator)