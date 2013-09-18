# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines logic-related tools.'''

import collections

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools


def all_equal(iterable, exhaustive=False):
    '''
    Return whether all elements in the iterable are equal to each other.
    
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
        pairs = sequence_tools.combinations(list(iterable), 2)
    else: # exhaustive is False
        pairs = cute_iter_tools.iterate_overlapping_subsequences(iterable)
        
    return all(a==b for (a, b) in pairs)


def get_equivalence_classes(iterable, key):
    '''
    Divide items in `iterable` to equivalence classes, using the key function.
    
    i.e. each item will be put in a set with all other items that had the same
    result when put through the `key` function.
    
    Returns a `dict` with keys being the results of the function, and the
    values being the sets of items with those values.
    '''
    key_function = \
             (lambda item: getattr(item, key)) if isinstance(key, str) else key
    equivalence_class_to_members = collections.defaultdict(set)
    for item in iterable:
        equivalence_class = key_function(item)
        equivalence_class_to_members[equivalence_class].add(item)
            
    return equivalence_class_to_members
        
      
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
        