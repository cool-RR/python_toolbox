# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines functions for manipulating iterators.'''
# todo: make something like `filter` except it returns first found, or raises
# exception

from __future__ import with_statement

import itertools
import __builtin__

from garlicsim.general_misc.infinity import infinity


def consecutive_pairs(iterable, wrap_around=False):
    '''
    Iterate over successive pairs from the iterable.
    
    If `wrap_around=True`, will include a `(last_item, first_item)` pair at the
    end.
        
    Example: if the iterable is [0, 1, 2, 3], then its `consecutive_pairs`
    would be `[(0, 1), (1, 2), (2, 3)]`. (Except it would be an iterator and
    not an actual list.)
    '''
    iterator = iter(iterable)
    
    try:
        first_item = iterator.next()
    except StopIteration:
        raise StopIteration
    
    old = first_item
    
    if not wrap_around:
        # If `wrap_around` is `False, we avoid holding a reference to
        # `first_item`, because it may need to be garbage-collected:
        del first_item 
    
    for current in iterator:
        yield (old, current)
        old = current
        
    if wrap_around:
        yield (current, first_item)
        
    
def shorten(iterable, n):
    '''
    Shorten an iterable to length `n`.
    
    Iterate over the given iterable, but stop after `n` iterations (Or when the
    iterable stops iteration by itself.)
    
    `n` may be infinite.
    '''

    if n == infinity:
        for thing in iterable:
            yield thing
        raise StopIteration
    
    assert isinstance(n, int)

    if n == 0:
        raise StopIteration
    
    for i, thing in enumerate(iterable):
        yield thing
        if i + 1 == n: # Checking `i + 1` to avoid pulling an extra item.
            raise StopIteration
        
        
def enumerate(reversible, reverse_index=False):
    '''
    Iterate over `(i, item)` pairs, where `i` is the index number of `item`.
    
    This is an extension of the builtin `enumerate`. What it allows is to get a
    reverse index, by specifying `reverse_index=True`. This causes `i` to count
    down to zero instead of up from zero, so the `i` of the last member will be
    zero.
    '''
    if reverse_index is False:
        return __builtin__.enumerate(reversible)
    else:
        my_list = list(__builtin__.enumerate(reversed(reversible)))
        my_list.reverse()
        return my_list

    
def is_iterable(thing):
    '''Return whether an object is iterable.'''
    if hasattr(type(thing), '__iter__'):
        return True
    else:
        try:
            iter(thing)
        except TypeError:
            return False
        else:
            return True
        

def get_length(iterable):
    '''
    Get the length of an iterable.
    
    If given an iterator, it will be exhausted.
    '''
    i = 0
    for thing in iterable:
        i += 1
    return i


def product(*args, **kwargs):
    '''
    Cartesian product of input iterables.

    Equivalent to nested for-loops in a generator expression. `product(A, B)`
    returns the same as `((x,y) for x in A for y in B)`.
    
    More examples:
    
        list(product('ABC', 'xy')) == ['Ax', 'Ay', 'Bx', 'By', 'Cx', 'Cy']
        
        list(product(range(2), repeat=2) == ['00', '01', '10', '11']
        
    '''
    # todo: revamp, probably take from stdlib
    pools = map(tuple, args) * kwargs.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def iter_with(iterable, context_manager):
    '''Iterate on `iterable`, `with`ing the context manager on every `next`.'''
    
    iterator = iter(iterable)
    
    while True:
        
        with context_manager:
            next_item = iterator.next()
            # You may notice that we are not `except`ing a `StopIteration`
            # here; If we get one, it'll just get propagated and end *this*
            # iterator. todo: I just realized this will probably cause a bug
            # where `__exit__` will get the `StopIteration`! Make failing tests
            # and fix.
        
        yield next_item
        
        
def izip_longest(*iterables, **kwargs):
    # This is a really obfuscated algorithm, simplify and/or explain
    fill_value = kwargs.get('fillvalue', None)
    def sentinel(counter=([fill_value] * (len(iterables) - 1)).pop):
        yield counter()
    fillers = itertools.repeat(fill_value)
    iterables = [itertools.chain(iterable, sentinel(), fillers) for iterable
                 in iterables]
    try:
        for tuple_ in itertools.izip(*iterables):
            yield tuple_
    except IndexError:
        raise StopIteration
