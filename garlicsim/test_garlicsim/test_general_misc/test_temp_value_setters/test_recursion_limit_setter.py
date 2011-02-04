# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Tests for `garlicsim.general_misc.temp_value_setters.TempRecursionLimitSetter`.
'''

from __future__ import with_statement

import sys

from garlicsim.general_misc import cute_testing

from garlicsim.general_misc.temp_value_setters import TempRecursionLimitSetter


def test():
    '''Test basic workings of `TempRecursionLimitSetter`.'''
    old_recursion_limit = sys.getrecursionlimit()
    assert sys.getrecursionlimit() == old_recursion_limit
    with TempRecursionLimitSetter(old_recursion_limit + 3):
        assert sys.getrecursionlimit() == old_recursion_limit + 3
    assert sys.getrecursionlimit() == old_recursion_limit


def test_as_decorator():
    '''Test `TempRecursionLimitSetter` when used as a decorator.'''
    old_recursion_limit = sys.getrecursionlimit()
    @TempRecursionLimitSetter(1234)
    def f():
        assert sys.getrecursionlimit() == 1234
    assert sys.getrecursionlimit() == old_recursion_limit
    f()
    assert sys.getrecursionlimit() == old_recursion_limit
    
    cute_testing.assert_polite_wrapper(f)