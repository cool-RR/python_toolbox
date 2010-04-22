# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module for doing a binary search in a sequence.

Todo: wrap all things in tuples?

todo: add option to specify cmp.

todo: i think `binary_search_by_index` should have the core logic, and the other
one will use it. I think this will save many sequence accesses, and some
sequences can be expensive.
'''

from .roundings import *

def binary_search_by_index(sequence, function, value, rounding=CLOSEST):
    '''
    Similiar to binary_search (refer to its documentation for more info).
    The difference is that instead of returning a result in terms of sequence
    items, it returns the indexes of these items in the sequence.
    ''' 
    if function is None:
        function = lambda x: x
    my_range = xrange(len(sequence))
    fixed_function = lambda index: function(sequence[index])
    result = binary_search(my_range, fixed_function, value, rounding)
    return result


def binary_search(sequence, function, value, CLOSEST):
    '''
    Does a binary search through a sequence.
    
    It is assumed that `function` is a montonic rising function on `sequence`.

    tododoc: decide where to put the following doc, if here or in the rounding
    classes:
    
    There are five options for the `rounding` parameter:
    
    * 'high': Gives the lowest sequence item which has value greater or equal
    to `value`.
    
    * 'low': Gives the highest sequence item which has value smaller or equal to
    `value`.
    
    * 'exact': Gives the item which has a value of exactly `value`.
    
    * 'closest': Gives the item that has value closest to `value`.
    
    * 'both': Gives a tuple (low, high) of the two items that surround `value`.
    If there's an exact match, gives it twice in the tuple, i.e. (match, match).
    
    For all rounding options, a return value of None is returned if no
    matching item is found. (In the case of rounding='both', either of the
    items in the tuple may be None)
    
    Note: This function uses None to express its inability to find any matches;
    Therefore, you better not use it on sequences in which None is a possible
    item.
    '''
    
    # todo: can break this into __binary_search_with_both_rounding

    # todo: i think this should be changed to return tuples
    
    assert isinstance(rounding, Rounding)
    
    if function is None:
        function = lambda x: x
    
    if not sequence:
        if rounding is BOTH:
            return (None, None)
        else:
            return None
    
    get = lambda number: function(sequence[number])

    low = 0
    high = len(sequence) - 1

    low_value, high_value = get(low), get(high)
    
    if low_value >= value:
        if rounding is BOTH:
            return [None if low_value > value else sequence[low], sequence[low]]
        if rounding in (HIGH, CLOSEST) or (low_value==value and rounding is EXACT):
            return sequence[low]
        else: # rounding is LOW or (rounding is EXACT and low_value!=value)
            return None
    if high_value <= value:
        if rounding is BOTH:
            return [sequence[high], None if high_value < value else sequence[high]]
        if rounding in (LOW, CLOSEST) or (low_value==value and rounding=='exact'):
            return sequence[high]
        else: # rounding is HIGH or (rounding is EXACT and low_value!=value)
            return None
        

    # Now we know the value is somewhere inside the sequence.
    
    
    while high - low > 1:
        medium = (low + high) // 2
        medium_value = get(medium)
        if medium_value > value:
            high = medium; high_value = medium_value
            continue
        if medium_value < value:
            low = medium; low_value = medium_value
            continue
        if medium_value == value:
            if rounding is BOTH:
                return (sequence[medium], sequence[medium])
            after_medium = medium + 1;
            after_medium_value = get(after_medium)
            if after_medium_value == value:
                low = medium; low_value = medium_value
                high = after_medium; high_value = after_medium_value
                break
            else: # get(medium+1) > value
                high = medium; high_value = medium_value
                low = medium - 1; low_value = get(low)
                break
    
    both = (sequence[low], sequence[high])
    
    return make_both_data_into_preferred_rounding(both, function,\
                                                  value, rounding)

def make_both_data_into_preferred_rounding(both, function, value, rounding):
    '''
    Refer to documentation of `binary_search` in this module.
    
    This function takes the return value from binary_search() with
    rounding=BOTH as the parameter both. It then gives the data with a
    different rounding, specified with the parameter `rounding`.
    '''
    if rounding is BOTH: return both
    elif rounding is LOW: return both[0]
    elif rounding is HIGH: return both[1]
    elif rounding is EXACT:
        return [state for state in both if
                (state is not None and function(state)==value)
                ][0]
    elif rounding is CLOSEST:
        if both[0] is None: return both[1]
        if both[1] is None: return both[0]
        distances = [abs(function(state)-value) for state in both]
        if distances[0] <= distances[1]:
            return both[0]
        else:
            return both[1]
        
        
