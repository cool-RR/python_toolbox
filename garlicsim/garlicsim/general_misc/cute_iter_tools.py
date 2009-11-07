# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines functions that may be useful when working with iterators.
'''

def pairs(iterable):
    '''
    Iterate over successive pairs from the iterable.
    
    Example:
    if the iterable is [0, 1, 2, 3], then its `pairs` would be
    [(0, 1), (1, 2), (2, 3)]. (Except it would be an iterator and not an actual
    list.)
    '''
    
    first_run = True
    old = None
    for current in iterable:
        if not first_run:
            yield (old, current)
        else:
            first_run = False
        old = current
        
def finitize(iterable, n):
    '''tododoc'''
    iterator = iter(iterable)
    for i in xrange(n):
        yield iterator.next()