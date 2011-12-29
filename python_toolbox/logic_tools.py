# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines logic-related tools.'''

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import sequence_tools


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
        pairs = cute_iter_tools.consecutive_pairs(iterable)
        
    return all(a==b for (a, b) in pairs)


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
        