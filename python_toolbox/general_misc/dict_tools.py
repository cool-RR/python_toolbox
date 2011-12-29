# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines several functions that may be useful when working with dicts.'''


def filter_items(d, condition):
    '''
    Get new dict with items from `d` that satisfy the `condition` functions.
    
    `condition` is a function that takes a key and a value.
    
    The newly created dict will be of the same class as `d`, e.g. if you passed
    an ordered dict as `d`, the result will be an ordered dict, using the
    correct order.
    '''
    # todo future: possibly shallow-copy `d` to allow for dict classes that
    # have more state, (like default factory.)
    dict_type = type(d) if (type(d).__name__ != 'dictproxy') else dict
    return dict_type(
        (key, value) for (key, value) in d.iteritems() if condition(key, value)
    )


def get_list(d, iterable):
    '''Get a list of values corresponding to an `iterable` of keys.'''
    return [d[key] for key in iterable]


def get_contained(d, container):
    '''Get a list of the values in the dict whose keys are in `container`.'''
    return [value for (key, value) in d.iteritems() if (key in container)]


def fancy_string(d, indent=0):
    '''Show a dict as a string, slightly nicer than dict.__repr__.'''

    small_space = ' ' * indent
    
    big_space = ' ' * (indent + 4)
    
    huge_space = ' ' * (indent + 8)
    
    def show(thing, indent=0):
        space = ' ' * indent
        enter_then_space = '\n' + space
        return repr(thing).replace('\n', enter_then_space)
    
    temp1 = (
        (big_space + repr(key) + ':\n' + huge_space + show(value, indent + 8))
        for(key, value) in d.items())
    
    temp2 = small_space + '{\n' + ',\n'.join(temp1) + '\n' + small_space +'}'
    
    return temp2
    

def reverse_with_set_values(d):
    '''
    Reverse the dict, with the values of the new dict being sets.
    
    Example:
    
        reverse_with_set_values({1: 2, 3: 4, 'meow': 2}) = \
            {2: set([1, 'meow']), 4: set([3])}
            
    '''
    new_dict = {}
    for key, value in d.iteritems():
        if value not in new_dict:
            new_dict[value] = []
        new_dict[value].append(key)
    
    # Making into sets:
    for key, value in new_dict.copy().iteritems():
        new_dict[key] = set(value)
        
    return new_dict


def devour_items(d):
    while d:
        yield d.popitem()

        
def devour(d):
    while d:
        yield d.pop()