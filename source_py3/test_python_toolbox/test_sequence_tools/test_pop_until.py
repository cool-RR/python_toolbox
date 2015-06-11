# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.sequence_tools import pop_until


def test():
    l = list(range(7))
    four = pop_until(l, condition=lambda i: i == 4)
    assert four == 4
    assert l == [0, 1, 2, 3]