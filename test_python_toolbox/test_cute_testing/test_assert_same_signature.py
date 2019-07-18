# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.cute_testing.assert_same_signature`.'''

from python_toolbox.third_party import decorator as decorator_module

from python_toolbox.cute_testing import (assert_same_signature,
                                                 RaiseAssertor,
                                                 Failure)


def test():
    '''Test the basic workings of `assert_same_signature`.'''

    def f(a, b=1, **kwargs):
        pass
    def g(a, b=1, **kwargs):
        pass
    def h(z):
        pass

    assert_same_signature(f, g)
    with RaiseAssertor(Failure):
        assert_same_signature(f, h)
    with RaiseAssertor(Failure):
        assert_same_signature(g, h)


    new_f = decorator_module.decorator(
        lambda *args, **kwargs: None,
        f
    )

    assert_same_signature(f, g, new_f)
    with RaiseAssertor(Failure):
        assert_same_signature(new_f, h)


    new_h = decorator_module.decorator(
        lambda *args, **kwargs: None,
        h
    )

    assert_same_signature(h, new_h)
    with RaiseAssertor(Failure):
        assert_same_signature(new_h, new_f)
    with RaiseAssertor(Failure):
        assert_same_signature(new_h, new_f, g)
    with RaiseAssertor(Failure):
        assert_same_signature(new_h, f)

    assert_same_signature(new_h, h, new_h, new_h)
