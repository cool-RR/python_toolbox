# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Module for tools to deal with segments, i.e. 2-tuples of numbers.'''

from python_toolbox import cute_iter_tools


def crop_segment(segment, base_segment):
    start, end = segment
    base_start, base_end = base_segment
    assert base_start <= start <= base_end or \
                                             base_start <= end <= base_end or \
                                         start <= base_start <= base_end <= end
           
    new_start = max((start, base_start))
    new_end = min((end, base_end))
    return (new_start, new_end)


def merge_segments(segments):
    assert all(len(segment) == 2 for segment in segments)
    sorted_segments = sorted(segments)
    if not sorted_segments:
        return ()
    
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


