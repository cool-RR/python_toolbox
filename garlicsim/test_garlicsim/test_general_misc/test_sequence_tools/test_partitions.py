# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `sequence_tools.partitions`.'''

from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc.sequence_tools import partitions


def test():
    r = xrange(8)
    assert partitions(r, 1) == partitions(r, n_partitions=8) == \
           [[0], [1], [2], [3], [4], [5], [6], [7]]
    assert partitions(r, 2) == partitions(r, n_partitions=4) == \
           [[0, 1], [2, 3], [4, 5], [6, 7]]
    assert partitions(r, 3) == partitions(r, n_partitions=3) == \
           [[0, 1, 2], [3, 4, 5], [6, 7]]
    assert partitions(r, 4) == partitions(r, n_partitions=2) == \
           [[0, 1, 2, 3], [4, 5, 6, 7]]
    assert partitions(r, 5) == [[0, 1, 2, 3, 4], [5, 6, 7]]
    assert partitions(r, 6) == [[0, 1, 2, 3, 4, 5], [6, 7]]
    assert partitions(r, 7) == [[0, 1, 2, 3, 4, 5, 6], [7]]
    assert partitions(r, 8) == partitions(r, 9) == partitions(r, 100) == \
           [[0, 1, 2, 3, 4, 5, 6, 7]] 
    