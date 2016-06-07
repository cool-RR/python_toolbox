# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.segment_tools import merge_segments

segments_to_fixed_segments = {
    (): (),
    ((0, 1),): ((0, 1),),
    ((0, 1), (0, 1)): ((0, 1),),
    ((0, 1), (0, 1), (0, 1)): ((0, 1),),
    ((0, 1), (0, 1), (3, 4)): ((0, 1), (3, 4)),
    ((0, 1), (0, 1), (3, 4), (4, 5)): ((0, 1), (3, 5)),
    ((0, 1), (0, 1), (3, 4), (4, 5), (4, 6), (6, 8), (6, 9), (6, 7), (11, 12)):
                                                    ((0, 1), (3, 9), (11, 12)),
    ((0, 10), (4, 16), (16, 17)): ((0, 17),),
    ((0, 10), (4, 16), (16, 17), (19, 20), (20, 22), (21, 30), (21, 24),
                                  (100, 110)): ((0, 17), (19, 30), (100, 110)),
    ((0, 10), (4, 7),): ((0, 10),),
    ((0, 10), (4, 7), (5, 8), (4, 5), (20, 22),): ((0, 10), (20, 22),),
}

def test_merge_segments():
    for segments, fixed_segments in segments_to_fixed_segments.items():
        assert merge_segments(segments) == \
                                  merge_segments(list(reversed(segments))) == \
                                                                 fixed_segments