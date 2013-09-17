# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import itertools

from python_toolbox.logic_tools import get_equivalence_classes


def test():
    assert get_equivalence_classes([1, 2, 3, 1j, 2j, 3j, 1+1j, 2+2j, 3+3j],
                                   abs) == {
        1: {1, 1j},
        2: {2, 2j},
        3: {3, 3j},
        2**0.5: {1 + 1j},
        8**0.5: {2 + 2j},
        18**0.5: {3 + 3j},
    }