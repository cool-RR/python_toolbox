# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines logic-related tools.'''

import collections
import itertools
import operator

from python_toolbox import cute_iter_tools


def all_equivalent(iterable, relation=operator.eq, *, exhaustive=False):
    '''
    Return whether all elements in the iterable are equivalent to each other.
    
    By default "equivalent" means they're equal to each other in Python. You
    can set a different relation to the `relation` argument, as a function that
    accepts two arguments and returns whether they're equivalent or not. You
    can use this, for example, to test if all items are NOT equal by passing in
    `relation=operator.ne`.
    
    If `exhaustive` is set to `False`, it's assumed that the equality relation
    is transitive, therefore not every member is tested against every other
    member. So in a list of size `n`, `n-1` equality checks will be made.
    
    If `exhaustive` is set to `True`, every member will be checked against
    every other member. So in a list of size `n`, `(n*(n-1))/2` equality checks
    will be made.
    '''
    # todo: Maybe I should simply check if `len(set(iterable)) == 1`? Will not
    # work for unhashables.
    
    if exhaustive is True:
        items = tuple(iterable)
        if len(items) <= 1:
            return True
        from python_toolbox import combi
        pairs = tuple(
            items * comb for comb in combi.CombSpace(len(items), 2)
        )
        # Can't feed the items directly to `CombSpace` because they might not
        # be hashable.
    else: # exhaustive is False
        pairs = cute_iter_tools.iterate_overlapping_subsequences(iterable)
        
    return all(itertools.starmap(relation, pairs))


def get_equivalence_classes(iterable, key=None, container=set,
                            use_ordered_dict=False, sort_ordered_dict=False):
    '''
    Divide items in `iterable` to equivalence classes, using the key function.
    
    Each item will be put in a set with all other items that had the same
    result when put through the `key` function.
    
    Example:
    
        >>> get_equivalence_classes(range(10), lambda x: x % 3)
        {0: {0, 9, 3, 6}, 1: {1, 4, 7}, 2: {8, 2, 5}}
        {2: {1, 'meow'}, 4: {3}}
        
    
    Returns a `dict` with keys being the results of the function, and the
    values being the sets of items with those values.
    
    Alternate usages:
    
        Instead of a key function you may pass in an attribute name as a
        string, and that attribute will be taken from each item as the key.
        
        Instead of an iterable and a key function you may pass in a `dict` (or
        similar mapping) into `iterable`, without specifying a `key`, and the
        value of each item in the `dict` will be used as the key.
        
        Example:
        
            >>> get_equivalence_classes({1: 2, 3: 4, 'meow': 2})
            {2: {1, 'meow'}, 4: {3}}
            
    
    If you'd like the result to be in an `OrderedDict`, specify
    `use_ordered_dict=True`, and the items will be ordered according to
    insertion order. If you'd like that `OrderedDict` to be sorted, pass in
    `sort_ordered_dict=True`. (It automatically implies
    `use_ordered_dict=True`.) You can also pass in a sorting key function or
    attribute name as the `sort_ordered_dict` argument.
    '''
    
    from python_toolbox import comparison_tools
    
    ### Pre-processing input: #################################################
    #                                                                         #
    if key is None:
        if isinstance(iterable, collections.Mapping):
            d = iterable
        else:
            try:
                d = dict(iterable)
            except ValueError:
                raise Exception(
                    "You can't put in a non-dict without also supplying a "
                    "`key` function. We need to know which key to use."
                )
    else: # key is not None
        assert cute_iter_tools.is_iterable(iterable)
        key_function = comparison_tools.process_key_function_or_attribute_name(
            key
        )
        d = {key: key_function(key) for key in iterable}
    #                                                                         #
    ### Finished pre-processing input. ########################################
    
    if use_ordered_dict or sort_ordered_dict:
        from python_toolbox import nifty_collections
        new_dict = nifty_collections.OrderedDict()
    else:
        new_dict = {}
    for key, value in d.items():
        new_dict.setdefault(value, []).append(key)
    
    # Making into desired container:
    for key, value in new_dict.copy().items():
        new_dict[key] = container(value)
        
    if sort_ordered_dict:
        if isinstance(sort_ordered_dict, (collections.Callable, str)):
            key_function = comparison_tools. \
                      process_key_function_or_attribute_name(sort_ordered_dict)
            new_dict.sort(key_function)
        elif sort_ordered_dict is True:
            new_dict.sort()
        return new_dict
    
    else:
        return new_dict

        
      
def logic_max(iterable, relation=lambda a, b: (a >= b)):
    '''
    Get a list of maximums from the iterable.
    
    That is, get all items that are bigger-or-equal to all the items in the
    iterable.
    
    `relation` is allowed to be a partial order.
    '''
    sequence = list(iterable)
    
    maximal_elements = []
    
    for candidate in sequence:
        if all(relation(candidate, thing) for thing in sequence):
            maximal_elements.append(candidate)
    
    return maximal_elements
        
        
        
    