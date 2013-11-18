# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines functions for manipulating iterators.'''
# todo: make something like `filter` except it returns first found, or raises
# exception

import collections
import itertools
import builtins


infinity = float('inf')


def iterate_overlapping_subsequences(iterable, length=2, wrap_around=False):
    '''
    Iterate over overlapping subsequences from the iterable.
        
    Example: if the iterable is [0, 1, 2, 3], then the result would be
    `[(0, 1), (1, 2), (2, 3)]`. (Except it would be an iterator and not an
    actual list.)
    
    With a length of 3, the result would be an iterator of `[(0, 1, 2), (1,
    2, 3)]`.
    
    If `wrap_around=True`, the result would be `[(0, 1, 2), (1,
    2, 3), (2, 3, 0), (3, 0, 1)]`.
    '''
    if length == 1:
        yield from iterable
    
    assert length >= 2
    
    iterator = iter(iterable)
    
    first_items = get_items(iterator, length)
    if len(first_items) < length:
        if wrap_around:
            raise NotImplementedError(
                '`length` is greater than the length of the iterable, and '
                '`wrap_around` is set to `True`. Behavior for this is not '
                'implemented, because it would require repeating some members '
                'more than once.'
            )
        else:
            raise StopIteration
            
    if wrap_around:
        first_items_except_last = first_items[:-1]
        iterator = itertools.chain(iterator, first_items_except_last)
            
    deque = collections.deque(first_items)
    yield first_items
    
    # Allow `first_items` to be garbage-collected:
    del first_items
    # (Assuming `wrap_around` is `True`, because if it's `False` then all the
    # first items except the last will stay saved in
    # `first_items_except_last`.)
    
    for current in iterator:
        deque.popleft()
        deque.append(current)
        yield tuple(deque)
        
    
def shorten(iterable, n):
    '''
    Shorten an iterable to length `n`.
    
    Iterate over the given iterable, but stop after `n` iterations (Or when the
    iterable stops iteration by itself.)
    
    `n` may be infinite.
    '''

    if n == infinity:
        yield from iterable
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
        return builtins.enumerate(reversible)
    else:
        my_list = list(builtins.enumerate(reversed(reversible)))
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
    pools = list(map(tuple, args)) * kwargs.get('repeat', 1)
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
            next_item = next(iterator)
            # You may notice that we are not `except`ing a `StopIteration`
            # here; If we get one, it'll just get propagated and end *this*
            # iterator. todo: I just realized this will probably cause a bug
            # where `__exit__` will get the `StopIteration`! Make failing tests
            # and fix.
        
        yield next_item
        
        
def izip_longest(*iterables, **kwargs):
    '''
    izip_longest(iter1 [,iter2 [...]], [fillvalue=None]) -> izip_longest object
    
    Return an `izip_longest` object whose `.__next__()` method returns a
    `tuple` where the i-th element comes from the i-th iterable argument. The
    `.__next__()` method continues until the longest iterable in the argument
    sequence is exhausted and then it raises `StopIteration`. When the shorter
    iterables are exhausted, `fillvalue` is substituted in their place. The
    `fillvalue` defaults to `None` or can be specified by a keyword argument.
    '''    
    # This is a really obfuscated algorithm, simplify and/or explain
    fill_value = kwargs.get('fillvalue', None)
    def sentinel(counter=([fill_value] * (len(iterables) - 1)).pop):
        yield counter()
    fillers = itertools.repeat(fill_value)
    iterables = [itertools.chain(iterable, sentinel(), fillers) for iterable
                 in iterables]
    try:
        yield from zip(*iterables)
    except IndexError:
        raise StopIteration


def get_items(iterable, n, container_type=tuple):
    '''
    Get the next `n` items from the iterable as a `tuple`.
    
    If there are less than `n` items, no exception will be raised. Whatever
    items are there will be returned.
    
    If you pass in a different kind of container than `tuple` as
    `container_type`, it'll be used to wrap the results.
    '''
    return container_type(shorten(iterable, n))


def double_filter(filter_function, iterable):
    '''
    Filter an `iterable` into two lists according to a `filter_function`.
    
    This is similar to the builtin `filter`, except it returns a tuple of two
    iterators, the first iterating on items that passed the filter function,
    and the second iterating on items that didn't.
    '''
    iterator = iter(iterable)
    
    true_deque = collections.deque()
    false_deque = collections.deque()
    
    def process_value():
        value = next(iterator)
        if filter_function(value):
            true_deque.append(value)
        else:
            false_deque.append(value)
    
    def make_true_iterator():
        while True:
            try:
                yield true_deque.popleft()
            except IndexError:
                try:
                    process_value()
                except StopIteration:
                    break

    def make_false_iterator():
        while True:
            try:
                yield false_deque.popleft()
            except IndexError:
                try:
                    process_value()
                except StopIteration:
                    break
                
    return (make_true_iterator(), make_false_iterator())



def get_ratio(filter_function, iterable):
    '''Get the ratio of `iterable` items that pass `filter_function`.'''
    if isinstance(filter_function, str):
        attribute_name = filter_function
        filter_function = lambda item: getattr(item, attribute_name, None)
    n_total_items = 0
    n_passed_items = 0
    for item in iterable:
        n_total_items += 1
        if filter_function(item):
            n_passed_items += 1
    return n_passed_items / n_total_items
    

def fill(iterable, fill_value=None, fill_value_maker=None, length=infinity,
         sequence_type=None):
    '''
    Iterate on `iterable`, and after it's exhaused, yield fill values.
    
    If `fill_value_maker` is given, it's used to create fill values
    dynamically. (Useful if your fill value is `[]` and you don't want to use
    many copies of the same list.)
    
    If `length` is given, shortens the iterator to that length.
    
    If `sequence_type` is given, instead of returning an iterator, this
    function will return a sequenceo of that type.
    '''
    iterator = _fill(iterable, fill_value=fill_value,
                     fill_value_maker=fill_value_maker, 
                     length=length)
    
    if sequence_type is None:
        return iterator
    else:
        return sequence_type(iterator)
    
    
def _fill(iterable, fill_value=None, fill_value_maker=None, length=infinity):
    if fill_value_maker is not None:
        assert fill_value is None
    else:
        fill_value_maker = lambda: fill_value
        
    iterator = iter(iterable)
    iterator_exhausted = False
    
    for i in itertools.count():
        if i >= length:
            raise StopIteration
        
        if iterator_exhausted:
            yield fill_value_maker()
        else:
            try:
                yield next(iterator)
            except StopIteration:
                iterator_exhausted = True
                yield fill_value_maker()
                
    
def get_single_if_any(iterable,
                      exception_on_multiple=Exception('More than one value '
                                                      'not allowed.')):
    '''
    Get the single item of `iterable`, if any.
    
    If `iterable` has one item, return it. If it's empty, get `None`. If it has
    more than one item, raise an exception. (Unless
    `exception_on_multiple=None`.)
    '''
    assert isinstance(exception_on_multiple, Exception) or \
                                                  exception_on_multiple is None
    iterator = iter(iterable)
    try:
        first_item = next(iterator)
    except StopIteration:
        return None
    else:
        if exception_on_multiple:
            try:
                second_item = next(iterator)
            except StopIteration:
                return first_item
            else:
                raise exception_on_multiple
        else: # not exception_on_multiple
            return first_item