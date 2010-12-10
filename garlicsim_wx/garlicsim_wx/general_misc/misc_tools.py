from __future__ import division

import os.path

from garlicsim.general_misc import cute_iter_tools


def find_clear_place_on_circle(circle_points, circle_size=1):

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
    
    result = winner + (maximum_clear_space / 2)
    
    return result
        
    
def add_extension_if_plain(path, extension):
    
    if extension:
        assert extension.startswith('.')
    
    (without_extension, existing_extension) = os.path.splitext(path)
    if existing_extension:
        return path
    else: # not existing_extension
        return without_extension + extension