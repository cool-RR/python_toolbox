# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines logic-related tools.
'''

import garlicsim.general_misc.cute_iter_tools as cute_iter_tools


def all_equal(iterable):
    '''
    Return whether all elements in the iterable are equal to each other.
    
    It is assumed that the equality relation is transitive, therefore not every
    member is tested against every other member. In a list of size n, n-1
    equality checks will be made.
    '''
    return all(a==b for (a, b) in cute_iter_tools.pairs(iterable))

