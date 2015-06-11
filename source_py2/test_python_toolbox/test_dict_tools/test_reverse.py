# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox import dict_tools


def test():
    assert dict_tools.reverse({'one': 1, 'two': 2, 'three': 3}) == \
                                               {1: 'one', 2: 'two', 3: 'three'}
    assert dict_tools.reverse({}) == {}
    with cute_testing.RaiseAssertor():
        dict_tools.reverse({1: 0, 2: 0})
    with cute_testing.RaiseAssertor():
        dict_tools.reverse({1: []})
