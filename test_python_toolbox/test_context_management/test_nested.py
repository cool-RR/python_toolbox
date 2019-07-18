# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Test the `python_toolbox.context_management.nested` function.'''

from python_toolbox import freezing
from python_toolbox import cute_testing

from python_toolbox.context_management import (BlankContextManager, nested,
                                               as_reentrant)

get_depth_counting_context_manager = \
                                    lambda: as_reentrant(BlankContextManager())


def test_nested():
    '''Test the basic workings of `nested`.'''

    a = get_depth_counting_context_manager()
    b = get_depth_counting_context_manager()
    c = get_depth_counting_context_manager()

    with nested(a):
        assert (a.depth, b.depth, c.depth) == (1, 0, 0)
        with nested(a, b):
            assert (a.depth, b.depth, c.depth) == (2, 1, 0)
            with nested(a, b, c):
                assert (a.depth, b.depth, c.depth) == (3, 2, 1)

        with nested(c):
            assert (a.depth, b.depth, c.depth) == (1, 0, 1)

    assert (a.depth, b.depth, c.depth) == (0, 0, 0)

    ###########################################################################

    freezer_a = freezing.Freezer()
    freezer_b = freezing.Freezer()
    freezer_c = freezing.Freezer()
    freezer_d = freezing.Freezer()

    freezers = (freezer_a, freezer_b, freezer_c)

    assert freezer_a.frozen == freezer_b.frozen == freezer_c.frozen == \
                                                          freezer_d.frozen == 0

    with nested(*freezers):
        assert freezer_a.frozen == freezer_b.frozen == freezer_c.frozen == 1
        assert freezer_d.frozen == 0

    assert freezer_a.frozen == freezer_b.frozen == freezer_c.frozen == \
               freezer_d.frozen == 0

