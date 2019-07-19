# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Module for tools to deal with segments, i.e. 2-tuples of numbers.'''

from python_toolbox import cute_iter_tools


def crop_segment(segment, base_segment):
    '''
    Crop `segment` to fit inside `base_segment`.

    This means that if it was partially outside of `base_segment`, that portion
    would be cut off and you'll get only the intersection of `segment` and
    `base_segment`.

    Example:

        >>> crop_segment((7, 17), (10, 20))
        (10, 17)

    '''
    start, end = segment
    base_start, base_end = base_segment
    if not (base_start <= start <= base_end or \
            base_start <= end <= base_end or \
            start <= base_start <= base_end <= end):
        raise Exception(f'{segment} is not touching {base_segment}')

    new_start = max((start, base_start))
    new_end = min((end, base_end))
    return (new_start, new_end)


def merge_segments(segments):
    '''
    "Clean" a bunch of segments by removing any shared portions.

    This function takes an iterable of segments and returns a cleaned one in
    which any duplicated portions were removed. Some segments which were
    contained in others would be removed completely, while other segments that
    touched each other would be merged.

    Example:

        >>> merge_segments((0, 10), (4, 16), (16, 17), (30, 40))
        ((0, 17), (30, 40))

    '''
    sorted_segments = sorted(segments)
    assert all(len(segment) == 2 for segment in sorted_segments)

    fixed_segments = []
    pushback_iterator = cute_iter_tools.PushbackIterator(sorted_segments)

    for first_segment_in_run in pushback_iterator: # (Sharing iterator with
                                                   #  other for loop.)
        current_maximum = first_segment_in_run[1]

        for segment in pushback_iterator: # (Sharing iterator with other for
                                          #  loop.)
            if segment[0] > current_maximum:
                pushback_iterator.push_back()
                break
            elif segment[1] > current_maximum:
                current_maximum = segment[1]

        fixed_segments.append((first_segment_in_run[0], current_maximum))


    return tuple(fixed_segments)


