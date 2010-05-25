# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines functions that may be useful when working with iterators.'''
# todo: make something like `filter` except it returns first found, or raises
# exception

import itertools
import __builtin__

from garlicsim.general_misc.infinity import Infinity


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

def orderless_combinations(iterable, n, start=0):
    '''
    Iterate over combinations of items from the iterable.

    `n` specifies the number of items. `start` specifies the member number from
    which to start giving combinations. (Keep the default of 0 for doing the
    whole iterable.)
    
    Example:
    
    orderless_combinations([1, 2, 3, 4], n=2) would be, in list form: [[1, 2],
    [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]].
    '''
    # todo: optimize or find 3rd party tool
    
    if n == 1:
        for thing in itertools.islice(iterable, start, None):
            yield [thing]
    for (i, thing) in itertools.islice(enumerate(iterable), start, None):
        for sub_result in orderless_combinations(iterable, n-1, start=i+1):
            yield [thing] + sub_result
    
    
def shorten(iterable, n):
    '''
    Shorten an iterator to length `n`.
    
    Iterate over the given iterable, but stop after `n` iterations (Or when the
    iterable stops iteration by itself.)
    
    `n` may be infinite.
    '''

    if n == Infinity:
        for thing in iterable:
            yield thing
        raise StopIteration
    
    assert isinstance(n, int)
    counter = 0
    for thing in iterable:
        if counter >= n: raise StopIteration
        yield thing
        counter += 1
        
        
def enumerate(reversable, reverse_index=False):
    '''
    Iterate over `(i, item)` pairs, where `i` is the index number of `item`.
    
    This is an extension of the builtin `enumerate`. What it allows is to get a
    reverse index, by specifying `reverse_index=True`. This causes `i` to count
    down to zero instead of up from zero, so the `i` of the last member will be
    zero.
    '''
    if reverse_index is False:
        return __builtin__.enumerate(reversable)
    else:
        my_list = list(__builtin__.enumerate(reversed(reversable)))
        my_list.reverse()
        return my_list

    
def is_iterable(thing):
    '''Return whether an object is iterable.'''
    return hasattr(thing, '__iter__')


def get_length(iterable):
    '''Get the length of an iterable.'''
    i = 0
    for thing in iterable:
        i += 1
    return i


def product(*args, **kwargs):
    '''
    Cartesian product of input iterables.

    Equivalent to nested for-loops in a generator expression. For example,
    `product(A, B)` returns the same as ((x,y) for x in A for y in B).
    
    product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    '''
    pools = map(tuple, args) * kwargs.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)
