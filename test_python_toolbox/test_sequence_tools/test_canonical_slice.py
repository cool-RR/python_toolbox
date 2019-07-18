# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import math_tools

from python_toolbox.sequence_tools import CanonicalSlice


infinity = float('inf')


def test():

    r1 = list(range(5))
    r2 = list(range(2, 10))
    r3 = list(range(100, 3, -7))
    ranges = [r1, r2, r3]

    slices = [slice(3), slice(5), slice(9), slice(1, 4), slice(4, 7),
              slice(6, 2), slice(1, 4, 1), slice(1, 5, 3), slice(6, 2, 3),
              slice(6, 2, -3),  slice(8, 2, -1), slice(2, 5, -2),
              slice(None, 5, -2), slice(6, None, -2), slice(8, 4, None),
              slice(None, None, -2)]

    for slice_ in slices:
        canonical_slice = CanonicalSlice(slice_)

        # Replacing `infinity` with huge number cause Python's lists can't
        # handle `infinity`:
        if abs(canonical_slice.start) == infinity:
            start = 10**10 * math_tools.get_sign(canonical_slice.start)
        if abs(canonical_slice.stop) == infinity:
            stop = 10**10 * math_tools.get_sign(canonical_slice.stop)
        if abs(canonical_slice.step) == infinity:
            step = 10**10 * math_tools.get_sign(canonical_slice.step)
        #######################################################################

        assert [canonical_slice.start, canonical_slice.stop,
                canonical_slice.step].count(None) == 0

        for range_ in ranges:
            assert range_[slice_] == range_[canonical_slice.slice_]