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
        
def shorten(iterable, n):
    '''
    Shorten an iterator to length n.
    
    Iterate over the given iterable, but stop after n iterations (Or when the
    iterable stops iteration by itself.)
    
    todo: make possible for n to be infinite.
    '''
    
    assert isinstance(n, int)
    counter = 0
    for thing in iterable:
        if counter >= n: raise StopIteration
        yield thing
        counter += 1
        
