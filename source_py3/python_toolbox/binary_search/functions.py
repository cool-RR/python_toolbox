# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Module for doing a binary search in a sequence.'''

# Todo: wrap all things in tuples?
# 
# todo: add option to specify `cmp`.
# 
# todo: i think `binary_search_by_index` should have the core logic, and the
# other one will use it. I think this will save many sequence accesses, and
# some sequences can be expensive.
#
# todo: ensure there are no `if variable` checks where we're thinking of None
# but the variable might be False

from python_toolbox import misc_tools

from .roundings import (Rounding, roundings, LOW, LOW_IF_BOTH,
                        LOW_OTHERWISE_HIGH, HIGH, HIGH_IF_BOTH,
                        HIGH_OTHERWISE_LOW, EXACT, CLOSEST, CLOSEST_IF_BOTH,
                        BOTH)

def binary_search_by_index(sequence, value,
                           function=misc_tools.identity_function,
                           rounding=CLOSEST):
    '''
    Do a binary search, returning answer as index number.
    
    Similiar to binary_search (refer to its documentation for more info). The
    difference is that instead of returning a result in terms of sequence
    items, it returns the indexes of these items in the sequence.
    
    For documentation of rounding options, check `binary_search.roundings`.
    ''' 
    my_range = range(len(sequence))
    fixed_function = lambda index: function(sequence[index])
    result = binary_search(my_range, value, function=fixed_function,
                           rounding=rounding)
    return result


def _binary_search_both(sequence, value,
                        function=misc_tools.identity_function):
    '''
    Do a binary search through a sequence with the `BOTH` rounding.
    
    It is assumed that `function` is a strictly monotonic rising function on
    `sequence`.
    
    Note: This function uses `None` to express its inability to find any
    matches; therefore, you better not use it on sequences in which `None` is a
    possible item.
    '''
    # todo: i think this should be changed to return tuples
    
    ### Preparing: ############################################################
    #                                                                         #
    get = lambda number: function(sequence[number])

    low = 0
    high = len(sequence) - 1
    #                                                                         #
    ### Finished preparing. ###################################################
    
    ### Handling edge cases: ##################################################
    #                                                                         #
    if not sequence:
        return (None, None)
    
    low_value, high_value = get(low), get(high)
        
    if value in (low_value, high_value):
        return tuple((value, value))
    
    elif low_value > value:
        return tuple((None, sequence[low]))

    elif high_value < value:
        return (sequence[high], None)
    #                                                                         #
    ### Finished handling edge cases. #########################################
        
        
    # Now we know the value is somewhere inside the sequence.
    assert low_value < value < high_value
    
    while high - low > 1:
        medium = (low + high) // 2
        medium_value = get(medium)
        if medium_value > value:
            high, high_value = medium, medium_value
            continue
        if medium_value < value:
            low, low_value = medium, medium_value
            continue
        if medium_value == value:
            return (sequence[medium], sequence[medium])
    
    return (sequence[low], sequence[high])
    


def binary_search(sequence, value, function=misc_tools.identity_function,
                  rounding=CLOSEST):
    '''
    Do a binary search through a sequence.
    
    It is assumed that `function` is a strictly monotonic rising function on
    `sequence`.
    
    For all rounding options, a return value of None is returned if no matching
    item is found. (In the case of `rounding=BOTH`, either of the items in the
    tuple may be `None`)
    
    Note: This function uses `None` to express its inability to find any
    matches; therefore, you better not use it on sequences in which None is a
    possible item.
    
    For documentation of rounding options, check `binary_search.roundings`.
    '''
    
    from .binary_search_profile import BinarySearchProfile
    
    binary_search_profile = BinarySearchProfile(sequence, value,
                                                function=function)
    return binary_search_profile.results[rounding]


def make_both_data_into_preferred_rounding(
            both, value, function=misc_tools.identity_function, rounding=BOTH):
    '''
    Convert results gotten using `BOTH` to a different rounding option.
    
    This function takes the return value from `binary_search` (or other such
    functions) with `rounding=BOTH` as the parameter `both`. It then gives the
    data with a different rounding, specified with the parameter `rounding`.
    '''
    # todo optimize and organize: break to individual functions, put in
    # `BinarySearchProfile`
    if rounding is BOTH:
        return both
    
    elif rounding is LOW:
        return both[0]
    
    elif rounding is LOW_IF_BOTH:
        return both[0] if both[1] is not None else None
    
    elif rounding is LOW_OTHERWISE_HIGH:
        return both[0] if both[0] is not None else both[1]
    
    elif rounding is HIGH:
        return both[1]
    
    elif rounding is HIGH_IF_BOTH:
        return both[1] if both[0] is not None else None
    
    elif rounding is HIGH_OTHERWISE_LOW:
        return both[1] if both[1] is not None else both[0]
    
    elif rounding is EXACT:
        results = [item for item in both if
                   (item is not None and function(item) == value)]
        return results[0] if results else None
    
    elif rounding in (CLOSEST, CLOSEST_IF_BOTH):
        if rounding is CLOSEST_IF_BOTH:
            if None in both:
                return None
        if both[0] is None: return both[1]
        if both[1] is None: return both[0]
        distances = [abs(function(item)-value) for item in both]
        if distances[0] <= distances[1]:
            return both[0]
        else:
            return both[1]
        
        