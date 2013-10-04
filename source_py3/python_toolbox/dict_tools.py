# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines several functions that may be useful when working with dicts.'''

import collections

from python_toolbox import cute_iter_tools
from python_toolbox import comparison_tools


def filter_items(d, condition, force_dict_type=None):
    '''
    Get new dict with items from `d` that satisfy the `condition` functions.
    
    `condition` is a function that takes a key and a value.
    
    The newly created dict will be of the same class as `d`, e.g. if you passed
    an ordered dict as `d`, the result will be an ordered dict, using the
    correct order.
    '''
    # todo future: possibly shallow-copy `d` to allow for dict classes that
    # have more state, (like default factory.)
    if force_dict_type is not None:
        dict_type = force_dict_type
    else:
        dict_type = type(d) if (type(d).__name__ != 'dictproxy') else dict
    return dict_type(
        (key, value) for (key, value) in d.items() if condition(key, value)
    )


def get_list(d, iterable):
    '''Get a list of values corresponding to an `iterable` of keys.'''
    return [d[key] for key in iterable]


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
    

def reverse_with_set_values(d, sort=False):
    '''
    Reverse the dict, with the values of the new dict being sets.
    
    Example:
    
        reverse_with_set_values({1: 2, 3: 4, 'meow': 2}) == \
                                                       {2: {1, 'meow'}, 4: {3}}
            
    Instead of a dict you may also input a tuple in which the first item is an
    iterable and the second item is either a key function or an attribute name.
    A dict will be constructed from these and used.
    
    If you'd like the result dict to be sorted, pass `sort=True`, and you'll
    get a sorted `OrderedDict`. You can also specify the sorting key function
    or attribute name as the `sort` argument.
    '''
    ### Pre-processing input: #################################################
    #                                                                         #
    if hasattr(d, 'items'): # `d` is a dict
        fixed_dict = d
    else: # `d` is not a dict
        assert cute_iter_tools.is_iterable(d) and len(d) == 2
        iterable, key_function_or_attribute_name = d
        assert cute_iter_tools.is_iterable(iterable)
        key_function = comparison_tools.process_key_function_or_attribute_name(
            key_function_or_attribute_name
        )
        fixed_dict = {key: key_function(key) for key in iterable}
    #                                                                         #
    ### Finished pre-processing input. ########################################
    
    new_dict = {}
    for key, value in fixed_dict.items():
        if value not in new_dict:
            new_dict[value] = []
        new_dict[value].append(key)
    
    # Making into sets:
    for key, value in new_dict.copy().items():
        new_dict[key] = set(value)
        
    if sort:
        from python_toolbox import nifty_collections
        ordered_dict = nifty_collections.OrderedDict(new_dict)
        if isinstance(sort, (collections.Callable, str)):
            key_function = comparison_tools. \
                                   process_key_function_or_attribute_name(sort)
        else:
            assert sort is True
            key_function = None
        ordered_dict.sort(key_function)
        return ordered_dict
    else:
        return new_dict


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
            
            
        
    
    
    
    
    
    