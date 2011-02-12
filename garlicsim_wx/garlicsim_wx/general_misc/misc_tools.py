# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines miscellaneous tools.'''

from __future__ import division

import os.path

from garlicsim.general_misc import cute_iter_tools


def find_clear_place_on_circle(circle_points, circle_size=1):
    '''
    Find the point on a circle that's the farthest away from other points.
    
    Given an interval `(0, circle_size)` and a bunch of points in it, find a
    place for a new point that is as far away from the other points as
    possible. (Since this is a circle, there's wraparound, e.g. the end of the
    interval connects to the start.)
    '''

    # Before starting, taking care of two edge cases:
    if not circle_points:
        # Edge case: No points at all
        return circle_size / 2
    if len(circle_points) == 1:
        # Edge case: Only one point
        return (circle_points[0] + circle_size / 2) % circle_size
    
    sorted_circle_points = sorted(circle_points)
    last_point = sorted_circle_points[-1]
    if last_point >= circle_size:
        raise Exception("One of the points (%s) is bigger than the circle "
                        "size %s." % (last_point, circle_size))
    clear_space = {}
    
    for first_point, second_point in cute_iter_tools.consecutive_pairs(
        sorted_circle_points, wrap_around=True
        ):
        
        clear_space[first_point] = second_point - first_point
        
    # That's the only one that might be negative, so we ensure it's positive:
    clear_space[last_point] %= circle_size
    
    maximum_clear_space = max(clear_space.itervalues())
    
    winners = [key for (key, value) in clear_space.iteritems()
               if value == maximum_clear_space]
    
    winner = winners[0]
    
    result = (winner + (maximum_clear_space / 2)) % circle_size
    
    return result
        
    
def add_extension_if_plain(path, extension):
    '''Add `extenstion` to a file path if it doesn't have an extenstion.'''
    
    if extension:
        assert extension.startswith('.')
    
    (without_extension, existing_extension) = os.path.splitext(path)
    if existing_extension:
        return path
    else: # not existing_extension
        return without_extension + extension
    