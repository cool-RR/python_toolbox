# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for manipulating sequences.'''

import collections
import types
import itertools

from python_toolbox import math_tools


infinity = float('inf')


def are_equal_regardless_of_order(seq1, seq2):
    '''
    Do `seq1` and `seq2` contain the same elements, same number of times?
    
    Disregards order of elements.

    Currently will fail for items that have problems with comparing.
    '''
    return collections.Counter(seq1) == collections.Counter(seq2)


def flatten(iterable):
    '''
    Flatten a sequence, returning a sequence of all its items' items.

    For example, `flatten([[1, 2], [3], [4, 'meow']]) == [1, 2, 3, 4, 'meow']`.
    '''

    iterator = iter(iterable)
    try:
        first_item = next(iterator)
    except StopIteration:
        return []
    return sum(iterator, first_item)


def combinations(sequence, n=None, start=0):
    '''
    Iterate over combinations of items from the sequence.

    `n` specifies the number of items. (Use `None` for all possible sizes
    together.) `start` specifies the index number of the member from which to
    start giving combinations. (Keep the default of `start=0` for doing the
    whole sequence.)

    Example:

    `combinations([1, 2, 3, 4], n=2)` would be, in list form: `[[1, 2], [1, 3],
    [1, 4], [2, 3], [2, 4], [3, 4]]`.
    '''

    if n is None:
        length = len(sequence) - start
        iterators = (combinations(sequence, n=i, start=start) for i
                     in xrange(1, length + 1))
        for item in itertools.chain(*iterators):
            yield item

    elif n == 1:
        for thing in itertools.islice(sequence, start, None):
            yield [thing]
    else:
        assert n > 1
        for (i, thing) in itertools.islice(enumerate(sequence), start, None):
            for sub_result in combinations(sequence, n - 1, start=(i + 1)):
                yield [thing] + sub_result


class NO_FILL_VALUE(object):
    '''
    Sentinel that means: Don't fill last partition with default fill values.
    '''


def partitions(sequence, partition_size=None, n_partitions=None,
               allow_remainder=True, fill_value=NO_FILL_VALUE):
    '''
    Partition `sequence` into equal partitions of size `partition_size`, or
    determine size automatically given the number of partitions as
    `n_partitions`.

    If the sequence can't be divided into precisely equal partitions, the last
    partition will contain less members than all the other partitions.

    Example:

        >>> partitions([0, 1, 2, 3, 4], 2)
        [[0, 1], [2, 3], [4]]

    (You need to give *either* a `partition_size` *or* an `n_partitions`
    argument, not both.)

    Specify `allow_remainder=False` to enforce that the all the partition sizes
    be equal; if there's a remainder while `allow_remainder=False`, an
    exception will be raised.

    If you want the remainder partition to be of equal size with the other
    partitions, you can specify `fill_value` as the padding for the last
    partition. A specified value for `fill_value` implies
    `allow_remainder=True` and will cause an exception to be raised if
    specified with `allow_remainder=False`.

    Example:

        >>> partitions([0, 1, 2, 3, 4], 3, fill_value=None)
        [[0, 1, 2], [3, 4, None]]
        
    '''

    sequence_length = len(sequence)

    ### Validating input: #####################################################
    #                                                                         #
    if (partition_size is None) == (n_partitions is None):
        raise Exception('You must specify *either* `partition_size` *or* '
                        '`n_paritions`.')

    if fill_value != NO_FILL_VALUE and not allow_remainder:
        raise ValueError('`fill_value` cannot be specified if '
                         '`allow_remainder` is `False`.')

    remainder_length = sequence_length % (partition_size if partition_size
                                          is not None else n_partitions)

    if not allow_remainder and remainder_length > 0:
        raise Exception("You set `allow_remainder=False`, but there's a "
                        "reminder of %s left." % remainder_length)
    #                                                                         #
    ### Finished validating input. ############################################

    if partition_size is None:
        partition_size = math_tools.ceil_div(sequence_length, n_partitions)
    if n_partitions is None:
        n_partitions = math_tools.ceil_div(sequence_length, partition_size)

    enlarged_length = partition_size * n_partitions

    blocks = [sequence[i : i + partition_size] for i in
              xrange(0, enlarged_length, partition_size)]

    if fill_value != NO_FILL_VALUE and blocks:
        filler = itertools.repeat(fill_value,
                                  enlarged_length - sequence_length)
        blocks[-1].extend(filler)

    return blocks


def is_sequence(thing):
    '''Is `thing` a sequence, like `list` or `tuple`?'''
    return collections.Sequence.__instancecheck__(thing)


def is_mutable_sequence(thing):
    '''Is `thing` a mutable sequence, like `list`?'''
    return collections.MutableSequence.__instancecheck__(thing)


def is_immutable_sequence(thing):
    '''Is `thing` an immutable sequence, like `tuple`?'''
    return collections.Sequence.__instancecheck__(thing) and not \
           collections.MutableSequence.__instancecheck__(thing)


def parse_slice(s):
    '''
    Parse a `slice` object into a canonical `(start, stop, step)`.

    This is helpful because `slice`'s own `.start`, `.stop` and `.step` are
    sometimes specified as `None` for convenience, so Python will infer them
    automatically. Here we make them explicit.

    if `start` is `None`, it will be set to `0` (if the `step` is positive) or
    `infinity` (if the `step` is negative.)

    if `stop` is `None`, it will be set to `infinity` (if the `step` is
    positive) or `0` (if the `step` is negative.)

    If `step` is `None`, it will be changed to the default `1`.
    '''
    assert isinstance(s, slice)

    ### Parsing `step`:
    assert s.step != 0
    if s.step is None:
        step = 1
    else:
        step = s.step
    ###

    ### Parsing `start`:
    if s.start is not None:
        start = s.start
    else:
        assert s.start is None
        if step > 0:
            start = 0
        else:
            assert step < 0
            start = infinity
    ###

    ### Parsing `stop`:
    if s.stop is not None:
        stop = s.stop
    else:
        assert s.stop is None
        if step > 0:
            stop = infinity
        else:
            assert step < 0
            stop = -infinity
    ###

    return (start, stop, step)


def to_tuple(single_or_sequence, item_type=None, item_test=None):
    '''
    Convert an item or a sequence of items into a tuple of items.

    This is typically used in functions that request a sequence of items but
    are considerate enough to accept a single item and wrap it in a tuple
    `(item,)` themselves.

    This function figures out whether the user entered a sequence of items, in
    which case it will only be converted to a tuple and returned; or the user
    entered a single item, in which case a tuple `(item,)` will be returned.

    To aid this function in parsing, you may optionally specify `item_type`
    which is the type of the items, or alternatively `item_test` which is a
    callable that takes an object and returns whether it's a valid item. These
    are necessary only when your items might be sequences themselves.
    '''
    if (item_type is not None) and (item_test is not None):
        raise Exception('You may specify either `item_type` or '
                        '`item_test` but not both.')
    if item_test is not None:
        actual_item_test = item_test
    elif item_type is not None:
        assert isinstance(item_type, (type, types.ClassType))
        actual_item_test = \
            lambda candidate: isinstance(candidate, item_type)
    else:
        actual_item_test = None

    if actual_item_test is None:
        if is_sequence(single_or_sequence):
            return tuple(single_or_sequence)
        else:
            return (single_or_sequence,)
    else: # actual_item_test is not None
        if actual_item_test(single_or_sequence):
            return (single_or_sequence,)
        else:
            return tuple(single_or_sequence)


def pop_until(sequence, condition=bool):
    '''
    Look for item in `sequence` that passes `condition`, popping away others.
    
    When sequence is empty, propagates the `IndexError`.
    '''
    while True:
        item = sequence.pop()
        if condition(item):
            return item


def get_recurrences(sequence):
    '''
    Get a `dict` of all items that repeat at least twice.
    
    The values of the dict are the numbers of repititions of each item.    
    '''
    return {item: n_recurrences for item, n_recurrences in
            collections.Counter(sequence).most_common() if n_recurrences >= 2}
    
### Not using now, might want in future:

#def heads(sequence, include_empty=False, include_full=True):    
    #for i in range(0 if include_empty else 1, len(sequence)):
        #yield sequence[:i]
    #if include_full:
        #yield sequence[:]
