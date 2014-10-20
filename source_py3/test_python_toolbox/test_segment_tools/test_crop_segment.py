# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.segment_tools import crop_segment


base_segment = (10, 20)

segment_to_cropped_segment = {
    (0, 15): (10, 15),
    (0, 12): (10, 12),
    (0, 10 ** 10): (10, 20),
    (5, 10 ** 10): (10, 20),
    (10, 10 ** 10): (10, 20),
    (15, 17): (15, 17),
    (19, 20): (19, 20),
    (20, 23): (20, 20),
    (20, 10 ** 10): (20, 20),
}

bad_segments = (
    (0, 5), 
    (0, 7), 
    (23, 25),
    (10 ** 10, 10 ** 11)
)


def test():
    for segment, cropped_segment in segment_to_cropped_segment.items():
        assert crop_segment(segment, base_segment) == cropped_segment
    for bad_segment in bad_segments:
        with cute_testing.RaiseAssertor():
            cropped_segment(segment, base_segment)
    
    