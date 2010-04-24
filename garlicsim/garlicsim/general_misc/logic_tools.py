# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines logic-related tools.'''

import garlicsim.general_misc.cute_iter_tools as cute_iter_tools


def all_equal(iterable, exhaustive=False):
    '''
    Return whether all elements in the iterable are equal to each other.
    
    If `exhaustive` is set to False, it's assumed that the equality relation is
    transitive, therefore not every member is tested against every other member.
    So in a list of size n, n-1 equality checks will be made.
    
    If `exhaustive` is set to True, every member will be checked against every
    other member. So in a list of size n, (n*(n-1))/2 equality checks will be
    made.
    '''
    
    if exhaustive is True:
        pairs = cute_iter_tools.orderless_combinations(iterable, 2)        
    else: # exhaustive is False
        pairs = cute_iter_tools.consecutive_pairs(iterable)
        
    return all(a==b for (a, b) in pairs)