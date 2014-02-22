# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines functions for manipulating iterators.'''
# todo: make something like `filter` except it returns first found, or raises
# exception

import collections
import itertools
import builtins

infinity = float('inf')


def iterate_overlapping_subsequences(iterable, length=2, wrap_around=False,
                                     lazy_tuple=False):
    '''
    Iterate over overlapping subsequences from the iterable.
        
    Example: if the iterable is [0, 1, 2, 3], then the result would be
    `[(0, 1), (1, 2), (2, 3)]`. (Except it would be an iterator and not an
    actual list.)
    
    With a length of 3, the result would be an iterator of `[(0, 1, 2), (1,
    2, 3)]`.
    
    If `wrap_around=True`, the result would be `[(0, 1, 2), (1,
    2, 3), (2, 3, 0), (3, 0, 1)]`.
    
    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _iterate_overlapping_subsequences(
        iterable=iterable, length=length, wrap_around=wrap_around
    )

    if lazy_tuple:
        from python_toolbox import nifty_collections # Avoiding circular import.
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator


def _iterate_overlapping_subsequences(iterable, length, wrap_around):

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
        
    
def shorten(iterable, n, lazy_tuple=False):
    '''
    Shorten an iterable to length `n`.
    
    Iterate over the given iterable, but stop after `n` iterations (Or when the
    iterable stops iteration by itself.)
    
    `n` may be infinite.

    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _shorten(iterable=iterable, n=n)

    if lazy_tuple:
        from python_toolbox import nifty_collections # Avoiding circular import.
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator


def _shorten(iterable, n):

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
        
        
def enumerate(reversible, reverse_index=False, lazy_tuple=False):
    '''
    Iterate over `(i, item)` pairs, where `i` is the index number of `item`.
    
    This is an extension of the builtin `enumerate`. What it allows is to get a
    reverse index, by specifying `reverse_index=True`. This causes `i` to count
    down to zero instead of up from zero, so the `i` of the last member will be
    zero.
    
    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _enumerate(reversible=reversible, reverse_index=reverse_index)

    if lazy_tuple:
        from python_toolbox import nifty_collections # Avoiding circular import.
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator

    
def _enumerate(reversible, reverse_index):
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


def iter_with(iterable, context_manager, lazy_tuple=False):
    '''
    Iterate on `iterable`, `with`ing the context manager on every `next`.
    
    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _iter_with(iterable=iterable, context_manager=context_manager)

    if lazy_tuple:
        from python_toolbox import nifty_collections # Avoiding circular import.
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator

    
def _iter_with(iterable, context_manager):
    
    iterator = iter(iterable)
    
    while True:
        
        with context_manager:
            next_item = next(iterator)
            # Recycling `StopIteration` exception. (Assuming the context
            # manager doesn't have special treatment for it.)
        
        yield next_item
        
        
def get_items(iterable, n, container_type=tuple):
    '''
    Get the next `n` items from the iterable as a `tuple`.
    
    If there are less than `n` items, no exception will be raised. Whatever
    items are there will be returned.
    
    If you pass in a different kind of container than `tuple` as
    `container_type`, it'll be used to wrap the results.
    '''
    return container_type(shorten(iterable, n))


def double_filter(filter_function, iterable, lazy_tuple=False):
    '''
    Filter an `iterable` into two iterables according to a `filter_function`.
    
    This is similar to the builtin `filter`, except it returns a tuple of two
    iterators, the first iterating on items that passed the filter function,
    and the second iterating on items that didn't.
    
    Note that this function is not thread-safe. (You may not consume the two
    iterators on two separate threads.)
    
    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = iter(iterable)
    
    true_deque = collections.deque()
    false_deque = collections.deque()
    
    def make_true_iterator():
        while True:
            try:
                yield true_deque.popleft()
            except IndexError:
                value = next(iterator) # `StopIteration` exception recycled.
                if filter_function(value):
                    yield value
                else:
                    false_deque.append(value)

    def make_false_iterator():
        while True:
            try:
                yield false_deque.popleft()
            except IndexError:
                value = next(iterator) # `StopIteration` exception recycled.
                if filter_function(value):
                    true_deque.append(value)
                else:
                    yield value
                
    iterators = (make_true_iterator(), make_false_iterator())
    
    if lazy_tuple:
        from python_toolbox import nifty_collections # Avoiding circular import.
        return tuple(map(nifty_collections.LazyTuple, iterators))
    else:
        return iterators



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
         sequence_type=None, lazy_tuple=False):
    '''
    Iterate on `iterable`, and after it's exhaused, yield fill values.
    
    If `fill_value_maker` is given, it's used to create fill values
    dynamically. (Useful if your fill value is `[]` and you don't want to use
    many copies of the same list.)
    
    If `length` is given, shortens the iterator to that length.
    
    If `sequence_type` is given, instead of returning an iterator, this
    function will return a sequence of that type. If `lazy_tuple=True`, uses a
    `LazyTuple`. (Can't use both options together.)
    '''
    # Validating user input:
    assert (sequence_type is None) or (lazy_tuple is False)
    
    iterator = _fill(iterable, fill_value=fill_value,
                     fill_value_maker=fill_value_maker, 
                     length=length)
    
    if lazy_tuple:
        from python_toolbox import nifty_collections # Avoiding circular import.
        return nifty_collections.LazyTuple(iterator)
    elif sequence_type is None:
        return iterator
    else:
        return sequence_type(iterator)
    
    
def _fill(iterable, fill_value, fill_value_maker, length):
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
                
    
def call_until_exception(function, exception, lazy_tuple=False):
    '''
    Iterate on values returned from `function` until getting `exception`.
    
    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _call_until_exception(function, exception)
    if lazy_tuple:
        from python_toolbox import nifty_collections # Avoiding circular import.
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator
    

def _call_until_exception(function, exception):
    from python_toolbox import sequence_tools
    exceptions = sequence_tools.to_tuple(exception, item_type=type)
    try:
        while True:
            yield function()
    except exceptions:
        raise StopIteration

    
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