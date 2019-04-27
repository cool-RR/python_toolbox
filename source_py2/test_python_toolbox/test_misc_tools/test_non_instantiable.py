# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.misc_tools import NonInstantiable


def test():
    class MyNonInstantiable(NonInstantiable):
        pass

    with cute_testing.RaiseAssertor(exception_type=RuntimeError):
        MyNonInstantiable()