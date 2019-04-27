# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.combi import *


def test():
    selection_space = SelectionSpace(range(5))
    assert len(tuple(selection_space)) == len(selection_space) == 2 ** 5
    assert selection_space[0] == set()
    assert selection_space[-1] == set(range(5))

    for i, selection in enumerate(selection_space):
        assert selection in selection_space
        assert selection_space.index(selection) == i

    assert (1, 6) not in selection_space
    assert 'foo' not in selection_space
    assert 7 not in selection_space
    assert (1, 3, 4) in selection_space
    assert selection_space
    assert repr(selection_space) == '<SelectionSpace: range(0, 5)>'
    assert {SelectionSpace(range(4)), SelectionSpace(range(4)),
            SelectionSpace(range(5)), SelectionSpace(range(4))} == \
                           {SelectionSpace(range(4)), SelectionSpace(range(5))}

    assert SelectionSpace(range(5)) == SelectionSpace(range(5))
    assert SelectionSpace(range(5)) != SelectionSpace(range(4))
    assert SelectionSpace(range(5)) != SelectionSpace(range(5, 0, -1))



