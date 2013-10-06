# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.misc_tools import NonInstatiable


def test():
    class MyNonInstatiable(NonInstatiable):
        pass
    
    with cute_testing.RaiseAssertor(exception_type=RuntimeError):
        MyNonInstatiable()