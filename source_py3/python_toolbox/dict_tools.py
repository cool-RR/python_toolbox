# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines several functions that may be useful when working with dicts.'''

import collections

from python_toolbox import cute_iter_tools
from python_toolbox import comparison_tools


def filter_items(d, condition, double=False, force_dict_type=None):
    '''
    Get new dict with items from `d` that satisfy the `condition` functions.
    
    `condition` is a function that takes a key and a value.
    
    The newly created dict will be of the same class as `d`, e.g. if you passed
    an ordered dict as `d`, the result will be an ordered dict, using the
    correct order.
    
    Specify `double=True` to get a tuple of two dicts instead of one. The
    second dict will have all the rejected items.
    '''
    # todo future: possibly shallow-copy `d` to allow for dict classes that
    # have more state, (like default factory.)
    if force_dict_type is not None:
        dict_type = force_dict_type
    else:
        dict_type = type(d) if (type(d).__name__ != 'dictproxy') else dict
        
    if double:
        return tuple(
            map(
                dict_type,
                cute_iter_tools.double_filter(
                    lambda key_value: condition(key_value[0], key_value[1]),
                    d.items()
                )
            )
        )
    else:
        return dict_type(
            (key, value) for (key, value) in d.items() if condition(key, value)
        )


def get_tuple(d, iterable):
    '''Get a tuple of values corresponding to an `iterable` of keys.'''
    return tuple(d[key] for key in iterable)


def get_contained(d, container):
    '''Get a list of the values in the dict whose keys are in `container`.'''
    return [value for (key, value) in d.items() if (key in container)]


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
                                           for (key, value) in list(d.items()))
    
    temp2 = small_space + '{\n' + ',\n'.join(temp1) + '\n' + small_space +'}'
    
    return temp2
    


def devour_items(d):
    '''Iterator that pops (key, value) pairs from `d` until it's empty.'''
    while d:
        yield d.popitem()

        
def devour_keys(d):
    '''Iterator that pops keys from `d` until it's exhaused (i.e. empty).'''
    while d:
        key = next(iter(d.keys()))
        del d[key]
        yield key
        
        
def sum_dicts(dicts):
    '''
    Return the sum of a bunch of dicts i.e. all the dicts merged into one.
    
    If there are any collisions, the latest dicts in the sequence win.
    '''
    result = {}
    for dict_ in dicts:
        result.update(dict_)
    return result


def remove_keys(d, keys_to_remove):
    '''
    Remove keys from a dict.
    
    `keys_to_remove` is allowed to be either an iterable (in which case it will
    be iterated on and keys with the same name will be removed), a container
    (in which case this function will iterate over the keys of the dict, and if
    they're contained they'll be removed), or a filter function (in which case
    this function will iterate over the keys of the dict, and if they pass the
    filter function they'll be removed.)
    
    If key doesn't exist, doesn't raise an exception.    
    '''
    if isinstance(keys_to_remove, collections.Iterable):
        for key in keys_to_remove:
            try:
                del d[key]
            except KeyError:
                pass
    else:
        if isinstance(keys_to_remove, collections.Container):
            filter_function = lambda value: value in keys_to_remove
        else:
            assert isinstance(keys_to_remove, collections.Callable)
            filter_function = keys_to_remove
        for key in list(d.keys()):
            if filter_function(key):
                del d[key]
            
            
def get_sorted_values(d, key=None):
    '''
    Get the values of dict `d` as a `tuple` sorted by their respective keys.
    '''
    kwargs = {'key': key,} if key is not None else {}
    return get_tuple(d, sorted(d.keys(), **kwargs))
    
    
def reverse(d):
    '''
    Reverse a `dict`, creating a new `dict` where keys and values are switched.
    
    Example:
    
        >>> reverse({'one': 1, 'two': 2, 'three': 3})
        {1: 'one', 2: 'two', 3: 'three'})
        
    This function requires that:
    
      1. The values will be distinct, i.e. no value will appear more than once.
      2. All the values be hashable.
      
    '''
    new_d = {}
    for key, value in d.items():
        if value in new_d:
            raise Exception(
                "Value %s appeared twice! Once with a key of %s and then "
                "again with a key of %s. This function is intended only for "
                "dicts with distinct values." % (value, key, new_d[value])
            )
        new_d[value] = key
    return new_d
            
    