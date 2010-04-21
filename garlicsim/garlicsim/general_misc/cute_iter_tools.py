# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines functions that may be useful when working with iterators.
'''

import itertools
import __builtin__

def consecutive_pairs(iterable):
    '''
    Iterate over successive pairs from the iterable.
    
    Example: if the iterable is [0, 1, 2, 3], then its `consecutive_pairs` would
    be [(0, 1), (1, 2), (2, 3)]. (Except it would be an iterator and not an
    actual list.)
    '''
    
    first_run = True
    old = None
    for current in iterable:
        if not first_run:
            yield (old, current)
        else:
            first_run = False
        old = current

def orderless_combinations(iterable, n, start=0):#tododoc, optimize
    if n == 1:
        for thing in itertools.islice(iterable, start, None):
            yield [thing]
    # if not isinstance(iterable, list):
    #     iterable = list(iterable)
    for (i, thing) in itertools.islice(enumerate(iterable), start, None):
        for sub_result in orderless_combinations(iterable, n-1, start=i+1):
            yield [thing] + sub_result
    
    
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
        
def enumerate(reversable, reverse_index=False):
    if reverse_index is False:
        return __builtin__.enumerate(reversable)
    else:
        my_list = list(__builtin__.enumerate(reversed(reversable)))
        my_list.reverse()
        return my_list

def is_iterable(thing):
    return hasattr(thing, '__iter__')

def get_length(iterable):
    i = 0
    for thing in iterable:
        i += 1
    return i