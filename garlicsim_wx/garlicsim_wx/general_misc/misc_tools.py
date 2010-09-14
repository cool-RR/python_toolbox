from garlicsim.general_misc import cute_iter_tools

def find_clear_place_on_circle(circle_points, circle_size=1):
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
        
    clear_space[last_point] %= circle_size
    # That's the only one that might be negative
        
        