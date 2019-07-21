# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''A collection of tools for manipulating iterators.'''

from __future__ import generator_stop

import collections
import operator
import itertools
import builtins
import numbers

from python_toolbox import sequence_tools
from python_toolbox import misc_tools
from python_toolbox import math_tools

infinity = float('inf')


class _EMPTY_SENTINEL(misc_tools.NonInstantiable):
    pass


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
        from python_toolbox import nifty_collections
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator


def _iterate_overlapping_subsequences(iterable, length, wrap_around):

    if length == 1:
        yield from iterable
        return

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
            return

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


def shorten(iterable, length, lazy_tuple=False):
    '''
    Shorten an iterable to `length`.

    Iterate over the given iterable, but stop after `n` iterations (Or when the
    iterable stops iteration by itself.)

    `n` may be infinite.

    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _shorten(iterable=iterable, length=length)

    if lazy_tuple:
        from python_toolbox import nifty_collections
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator


def _shorten(iterable, length):

    if length == infinity:
        yield from iterable
        return

    assert isinstance(length, int)

    if length == 0:
        return

    for i, thing in enumerate(iterable):
        yield thing
        if i + 1 == length: # Checking `i + 1` to avoid pulling an extra item.
            return


def enumerate(iterable, reverse_index=False, lazy_tuple=False):
    '''
    Iterate over `(i, item)` pairs, where `i` is the index number of `item`.

    This is an extension of the builtin `enumerate`. What it allows is to get a
    reverse index, by specifying `reverse_index=True`. This causes `i` to count
    down to zero instead of up from zero, so the `i` of the last member will be
    zero.

    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _enumerate(iterable=iterable, reverse_index=reverse_index)

    if lazy_tuple:
        from python_toolbox import nifty_collections
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator


def _enumerate(iterable, reverse_index):
    if reverse_index is False:
        return builtins.enumerate(iterable)
    else:
        from python_toolbox import sequence_tools
        from python_toolbox import nifty_collections
        try:
            length = sequence_tools.get_length(iterable)
        except AttributeError:
            iterable = nifty_collections.LazyTuple(iterable)
            length = len(iterable)
        return zip(range(length - 1, -1, -1), iterable)


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
    for _ in iterable:
        i += 1
    return i


def iter_with(iterable, context_manager, lazy_tuple=False):
    '''
    Iterate on `iterable`, `with`ing the context manager on every `next`.

    If `lazy_tuple=True`, returns a `LazyTuple` rather than an iterator.
    '''
    iterator = _iter_with(iterable=iterable, context_manager=context_manager)

    if lazy_tuple:
        from python_toolbox import nifty_collections
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator


def _iter_with(iterable, context_manager):

    iterator = iter(iterable)

    while True:

        with context_manager:
            try:
                next_item = next(iterator)
            except StopIteration:
                return

        yield next_item


def get_items(iterable, n_items, container_type=tuple):
    '''
    Get the next `n_items` items from the iterable as a `tuple`.

    If there are less than `n` items, no exception will be raised. Whatever
    items are there will be returned.

    If you pass in a different kind of container than `tuple` as
    `container_type`, it'll be used to wrap the results.
    '''
    return container_type(shorten(iterable, n_items))


def double_filter(filter_function, iterable, lazy_tuple=False):
    '''
    Filter an `iterable` into two iterables according to a `filter_function`.

    This is similar to the builtin `filter`, except it returns a tuple of two
    iterators, the first iterating on items that passed the filter function,
    and the second iterating on items that didn't.

    Note that this function is not thread-safe. (You may not consume the two
    iterators on two separate threads.)

    If `lazy_tuple=True`, returns two `LazyTuple` objects rather than two
    iterator.
    '''
    iterator = iter(iterable)

    true_deque = collections.deque()
    false_deque = collections.deque()

    def make_true_iterator():
        while True:
            try:
                yield true_deque.popleft()
            except IndexError:
                try:
                    value = next(iterator)
                except StopIteration:
                    return
                if filter_function(value):
                    yield value
                else:
                    false_deque.append(value)

    def make_false_iterator():
        while True:
            try:
                yield false_deque.popleft()
            except IndexError:
                try:
                    value = next(iterator)
                except StopIteration:
                    return
                if filter_function(value):
                    true_deque.append(value)
                else:
                    yield value

    iterators = (make_true_iterator(), make_false_iterator())

    if lazy_tuple:
        from python_toolbox import nifty_collections
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
        from python_toolbox import nifty_collections
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
            return

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
        from python_toolbox import nifty_collections
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
        return


def get_single_if_any(iterable, *,
                      exception_on_multiple=True, none_on_multiple=False):
    '''
    Get the single item of `iterable`, if any.

    Default behavior: Get the first item from `iterable`, and ensure it doesn't
    have any more items (raise an exception if it does.)

    If you pass in `exception_on_multiple=False`: If `iterable` has more than
    one item, an exception won't be raised. The first value will be returned.

    If you pass in `none_on_multiple=True`: If `iterable` has more than one
    item, `None` will be returned regardless of the value of the first item.
    Note that passing `none_on_multiple=True` causes the
    `exception_on_multiple` argument to be ignored. (This is a bit ugly but I
    made it that way so you wouldn't have to manually pass
    `exception_on_multiple=False` in this case.)
    '''
    if none_on_multiple:
        exception_on_multiple = False
    iterator = iter(iterable)
    try:
        first_item = next(iterator)
    except StopIteration:
        return None
    else:
        if exception_on_multiple or none_on_multiple:
            try:
                second_item = next(iterator)
            except StopIteration:
                return first_item
            else:
                if none_on_multiple:
                    return None
                else:
                    assert exception_on_multiple
                    raise Exception('More than one value not allowed.')
        else:
            return first_item


def are_equal(*sequences, easy_types=(sequence_tools.CuteRange,)):
    '''
    Are the given sequences equal?

    This tries to make a cheap comparison between the sequences if possible,
    but if not, it goes over the sequences in parallel item-by-item and checks
    whether the items are all equal. A cheap comparison is attempted only if
    the sequences are all of the same type, and that type is in `easy_types`.
    (It's important to restrict `easy_types` only to types where equality
    between the sequences is the same as equality between every item in the
    sequences.)
    '''
    from python_toolbox import logic_tools
    sequence_types = set(map(type, sequences))

    # Trying cheap comparison:
    if len(sequence_types) == 1 and issubclass(
                                get_single_if_any(sequence_types), easy_types):
        return logic_tools.all_equivalent(sequences)

    # If cheap comparison didn't work, trying item-by-item comparison:
    zipped = itertools.zip_longest(*sequences,
                                   fillvalue=_EMPTY_SENTINEL)
    for values in zipped:
        # No need to explicitly check for `_EMPTY_SENTINEL`, it would just make
        # the following condition `False`, because it's impossible for all
        # values to be the sentinel.
        if not logic_tools.all_equivalent(values):
            return False
    else:
        return True


def is_sorted(iterable, *, rising=True, strict=False, key=None):
    '''
    Is `iterable` sorted?

    Goes over the iterable item by item and checks whether it's sorted. If one
    item breaks the order, returns `False` and stops iterating. If after going
    over all the items, they were all sorted, returns `True`.

    You may specify `rising=False` to check for a reverse ordering. (i.e. each
    item should be lower or equal than the last one.)

    You may specify `strict=True` to check for a strict order. (i.e. each item
    must be strictly bigger than the last one, or strictly smaller if
    `rising=False`.)

    You may specify a key function as the `key` argument.
    '''
    from python_toolbox import misc_tools
    if key is None:
        key = misc_tools.identity_function
    comparer = {(False, False): operator.ge,
                (False, True): operator.gt,
                (True, False): operator.le,
                (True, True): operator.lt,}[(rising, strict)]
    for key_of_first_item, key_of_second_item in \
                          iterate_overlapping_subsequences(map(key, iterable)):
        if not comparer(key_of_first_item, key_of_second_item):
            return False
    else:
        return True


class _PUSHBACK_SENTINEL(misc_tools.NonInstantiable):
    '''Sentinel used by `PushbackIterator` to say nothing was pushed back.'''

class PushbackIterator:
    '''
    Iterator allowing to push back the last item so it'll be yielded next time.

    Initialize `PushbackIterator` with your favorite iterator as the argument
    and it'll create an iterator wrapping it on which you can call
    `.push_back()` to have it take the recently yielded item and yield it again
    next time.

    Only one item may be pushed back at any time.
    '''

    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.last_item = _PUSHBACK_SENTINEL
        self.just_pushed_back = False

    def __next__(self):
        if self.just_pushed_back:
            assert self.last_item != _PUSHBACK_SENTINEL
            self.just_pushed_back = False
            return self.last_item
        else:
            self.last_item = next(self.iterator)
            return self.last_item

    __iter__ = lambda self: self

    def push_back(self):
        '''
        Push the last item back, so it'll come up in the next iteration.

        You can't push back twice without iterating, because we only save the
        last item and not any previous items.
        '''
        if self.last_item == _PUSHBACK_SENTINEL:
            raise Exception
        if self.just_pushed_back:
            raise Exception
        self.just_pushed_back = True



def iterate_pop(poppable, lazy_tuple=False):
    '''Iterate by doing `.pop()` until no more items.'''
    return call_until_exception(poppable.pop, IndexError,
                                lazy_tuple=lazy_tuple)

def iterate_popleft(left_poppable, lazy_tuple=False):
    '''Iterate by doing `.popleft()` until no more items.'''
    return call_until_exception(left_poppable.popleft, IndexError,
                                lazy_tuple=lazy_tuple)

def iterate_popitem(item_poppable, lazy_tuple=False):
    '''Iterate by doing `.popitem()` until no more items.'''
    return call_until_exception(item_poppable.popitem, KeyError,
                                lazy_tuple=lazy_tuple)



def zip_non_equal(iterables, lazy_tuple=False):
    '''
    Zip the iterables, but only yield the tuples where the items aren't equal.
    '''
    from python_toolbox import logic_tools
    iterator = (items for items in zip(*iterables)
                if not logic_tools.all_equivalent(items))

    if lazy_tuple:
        from python_toolbox import nifty_collections
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator
