# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
A module for doing a binary search in a sequence.

Todo: create a different mode where all objects are wrapped in a list/tuple
before being returned. This will allow this module to handle sequences that
have None as legitimate members.

todo: add option to specify cmp.
"""


def binary_search_by_index(sequence, function, value, rounding="Closest"):
    """
    Similiar to binary_search (refer to its documentation for more info).
    The difference is that instead of returning a result in terms of sequence
    items, it returns the indexes of these items in the sequence.
    """
    
    my_range = range(len(sequence))
    fixed_function = lambda index: function(sequence[index])
    result = binary_search(my_range, fixed_function, value, rounding)
    return result


def binary_search(sequence, function, value, rounding="Closest"):
    """
    Does a binary search through a sequence.
    
    It is assumed that `function` is a montonic rising function on `sequence`.

    There are five options for the "rounding" parameter:
    "High": Gives the lowest sequence item which has value greater than `value`
    "Low": Gives the highest sequence item which has value smaller than `value`
    "Exact": Gives the item which has a value of exactly `value`
    "Closest": Gives the item that has value closest to `value`
    "Both": Gives a tuple (low, high) of the two items that surround `value`.
    
    For all rounding options, a return value of None is returned if no
    matching item is found. (In the case of rounding="Both", either of the
    items in the tuple may be None)
    
    Note: This function uses None to express its inability to find any matches;
    Therefore, you better not use it on sequences in which None is a possible
    item.
    """
    assert rounding in ["High", "Low", "Exact", "Both", "Closest"]
    
    get = lambda number: function(sequence[number])

    low = 0
    high = len(sequence) - 1

    low_value, high_value = get(low), get(high)
    
    if low_value >= value:
        if rounding == "Both":
            return [None, sequence[low]]
        if rounding in ["High", "Closest"] or (low_value==value and rounding=="Exact"):
            return sequence[low]
        else: # rounding == "Low" or (rounding == "Exact" and low_value!=value)
            return None
    if high_value <= value:
        if rounding == "Both":
            return [sequence[high], None]
        if rounding in ["Low", "Closest"] or (low_value==value and rounding=="Exact"):
            return sequence[high]
        else: # rounding == "High" or (rounding == "Exact" and low_value!=value)
            return None
        
    """
    Now we know the value is somewhere inside the sequence.
    """
    
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
    """
    Refer to documentation of `binary_search` in this module.
    
    This function takes the return value from binary_search() with
    rounding="Both" as the parameter both. It then gives the data with a
    different rounding, specified with the parameter `rounding`.
    """
    if rounding == "Both": return both
    elif rounding == "Low": return both[0]
    elif rounding == "High": return both[1]
    elif rounding == "Exact": return [state for state in both if (state is not None and function(state)==value)][0]
    elif rounding == "Closest":
        if both[0] is None: return both[1]
        if both[1] is None: return both[0]
        distances = [abs(function(state)-value) for state in both]
        if distances[0] <= distances[1]:
            return both[0]
        else:
            return both[1]
        
        
