# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import dict_tools


def test():
    d = {1: 'a', 2: 'd', 3: 'j', 4: 'b',}
    assert dict_tools.get_sorted_values(d) == ('a', 'd', 'j', 'b')
    assert dict_tools.get_sorted_values(d, key=lambda x: -x) == \
                                                           ('b', 'j', 'd', 'a')