# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.sequence_tools import get_recurrences


def test():
    assert get_recurrences([]) == get_recurrences(range(10)) == \
                                             get_recurrences(range(100)) == {}
    assert get_recurrences((1, 1, 1, 2, 2, 3)) == {1: 3, 2: 2,}