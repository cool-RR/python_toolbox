# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for manipulating sequences.'''

import collections
import numbers
import types
import itertools
import random

from python_toolbox import math_tools
from python_toolbox import caching
from python_toolbox import misc_tools

infinity = float('inf')


def are_equal_regardless_of_order(seq1, seq2):
    '''
    Do `seq1` and `seq2` contain the same elements, same number of times?

    Disregards order of elements.

    Currently will fail for items that have problems with comparing.
    '''
    from python_toolbox import nifty_collections
    return nifty_collections.Bag(seq1) == nifty_collections.Bag(seq2)


def flatten(iterable):
    '''
    Flatten a sequence, returning a sequence of all its items' items.

    For example, `flatten([[1, 2], [3], [4, 'meow']]) == [1, 2, 3, 4, 'meow']`.
    '''
    # If that ain't a damn clever implementation, I don't know what is.
    iterator = iter(iterable)
    try:
        return sum(iterator, next(iterator))
    except StopIteration:
        return []


class NO_FILL_VALUE(misc_tools.NonInstantiable):
    '''
    Sentinel that means: Don't fill last partition with default fill values.
    '''


def partitions(sequence, partition_size=None, *, n_partitions=None,
               allow_remainder=True, larger_on_remainder=False,
               fill_value=NO_FILL_VALUE):
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

    By default, if there's a remainder, the last partition will be smaller than
    the others. (e.g. a sequence of 7 items, when partitioned into pairs, will
    have 3 pairs and then a partition with only 1 element.) Specify
    `larger_on_remainder=True` to make the last partition be a bigger partition
    in case there's a remainder. (e.g. a sequence of a 7 items divided into
    pairs would result in 2 pairs and one triplet.)

    If you want the remainder partition to be of equal size with the other
    partitions, you can specify `fill_value` as the padding for the last
    partition. A specified value for `fill_value` implies
    `allow_remainder=True` and will cause an exception to be raised if
    specified with `allow_remainder=False`.

    Example:

        >>> partitions([0, 1, 2, 3, 4], 3, fill_value='meow')
        [[0, 1, 2], [3, 4, 'meow']]

    '''

    sequence = ensure_iterable_is_sequence(sequence)

    sequence_length = len(sequence)

    ### Validating input: #####################################################
    #                                                                         #
    if (partition_size is None) + (n_partitions is None) != 1:
        raise Exception('You must specify *either* `partition_size` *or* '
                        '`n_paritions`.')

    remainder_length = sequence_length % (partition_size if partition_size
                                          is not None else n_partitions)

    if not allow_remainder and remainder_length > 0:
        raise Exception(f"You set `allow_remainder=False`, but there's a "
                        f"remainder of {remainder_length} left.")
    #                                                                         #
    ### Finished validating input. ############################################

    if partition_size is None:

        floored_partition_size, modulo = divmod(sequence_length,
                                                n_partitions)
        if modulo:
            if larger_on_remainder:
                partition_size = floored_partition_size
                n_partitions += 1
                # Extra partition will be joined into previous partition
            else:
                partition_size = floored_partition_size + 1
        else: # modulo == 0
            partition_size = floored_partition_size
    if n_partitions is None:
        n_partitions = math_tools.ceil_div(sequence_length, partition_size)

    naive_length = partition_size * n_partitions

    blocks = [sequence[i : i + partition_size] for i in
              range(0, naive_length, partition_size)]

    if naive_length != sequence_length:
        assert blocks
        if larger_on_remainder:
            if len(blocks) >= 2:
                small_block_to_append_back = blocks[-1]
                del blocks[-1]
                blocks[-1] += small_block_to_append_back
        elif fill_value != NO_FILL_VALUE: # (We use elif because fill is never
                                          # done if `larger_on_remainder=True`.)
            filler = itertools.repeat(fill_value,
                                      naive_length - sequence_length)
            blocks[-1].extend(filler)

    return blocks


def is_immutable_sequence(thing):
    '''Is `thing` an immutable sequence, like `tuple`?'''
    return isinstance(thing, collections.abc.Sequence) and not \
                             isinstance(thing, collections.abc.MutableSequence)



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

    You may optionally put multiple types in `item_type`, and each object would
    be required to match to at least one of them.
    '''
    if (item_type is not None) and (item_test is not None):
        raise Exception('You may specify either `item_type` or '
                        '`item_test` but not both.')
    if item_test is not None:
        actual_item_test = item_test
    elif item_type is not None:
        actual_item_test = \
            lambda candidate: isinstance(candidate, item_type)
    else:
        actual_item_test = None

    if actual_item_test is None:
        if isinstance(single_or_sequence, collections.abc.Sequence):
            return tuple(single_or_sequence)
        elif single_or_sequence is None:
            return tuple()
        else:
            return (single_or_sequence,)
    else: # actual_item_test is not None
        if actual_item_test(single_or_sequence):
            return (single_or_sequence,)
        elif single_or_sequence is None:
            return ()
        else:
            return tuple(single_or_sequence)


def pop_until(sequence, condition=bool):
    '''
    Look for item in `sequence` that passes `condition`, popping away others.

    When sequence is empty, propagates the `IndexError`.
    '''
    from python_toolbox import cute_iter_tools
    for item in cute_iter_tools.iterate_pop(sequence):
        if condition(item):
            return item


def get_recurrences(sequence):
    '''
    Get a `dict` of all items that repeat at least twice.

    The values of the dict are the numbers of repititions of each item.
    '''
    from python_toolbox import nifty_collections
    return {item: n_recurrences for item, n_recurrences in
            nifty_collections.Bag(sequence).most_common() if n_recurrences >= 2}


def ensure_iterable_is_immutable_sequence(iterable, default_type=tuple,
                                          unallowed_types=(bytes,)):
    '''
    Return a version of `iterable` that is an immutable sequence.

    If `iterable` is already an immutable sequence, it returns it as is;
    otherwise, it makes it into a `tuple`, or into any other data type
    specified in `default_type`.
    '''
    from python_toolbox import nifty_collections
    assert isinstance(iterable, collections.abc.Iterable)
    if isinstance(iterable, collections.abc.MutableSequence) or \
       isinstance(iterable, unallowed_types) or \
       not isinstance(iterable, collections.abc.Sequence):
        return default_type(iterable)
    else:
        return iterable


def ensure_iterable_is_sequence(iterable, default_type=tuple,
                                unallowed_types=(bytes,)):
    '''
    Return a version of `iterable` that is a sequence.

    If `iterable` is already a sequence, it returns it as is; otherwise, it
    makes it into a `tuple`, or into any other data type specified in
    `default_type`.
    '''
    assert isinstance(iterable, collections.abc.Iterable)
    if isinstance(iterable, collections.abc.Sequence) and \
       not isinstance(iterable, unallowed_types):
        return iterable
    else:
        return default_type(iterable)


class CuteSequenceMixin(misc_tools.AlternativeLengthMixin):
    '''A sequence mixin that adds extra functionality.'''
    def take_random(self):
        '''Take a random item from the sequence.'''
        return self[random.randint(0, get_length(self) - 1)]
    def __contains__(self, item):
        try: self.index(item)
        except ValueError: return False
        else: return True



class CuteSequence(CuteSequenceMixin, collections.abc.Sequence):
    '''A sequence type that adds extra functionality.'''


def get_length(sequence):
    '''Get the length of a sequence.'''
    return sequence.length if hasattr(sequence, 'length') else len(sequence)


def divide_to_slices(sequence, n_slices):
    '''
    Divide a sequence to slices.

    Example:

        >>> divide_to_slices(range(10), 3)
        [range(0, 4), range(4, 7), range(7, 10)]

    '''
    from python_toolbox import cute_iter_tools

    assert isinstance(n_slices, numbers.Integral)
    assert n_slices >= 1

    sequence_length = get_length(sequence)
    base_slice_length, remainder = divmod(sequence_length, n_slices)
    indices = [0]
    for i in range(n_slices):
        indices.append(indices[-1] + base_slice_length + (remainder > i))
    assert len(indices) == n_slices + 1
    assert indices[0] == 0
    assert indices[-1] == sequence_length
    return [sequence[x:y] for x, y in
                     cute_iter_tools.iterate_overlapping_subsequences(indices)]


def is_subsequence(big_sequence, small_sequence):
    '''
    Check whether `small_sequence` is a subsequence of `big_sequence`.

    For example:

        >>> is_subsequence([1, 2, 3, 4], [2, 3])
        True
        >>> is_subsequence([1, 2, 3, 4], [4, 5])
        False

    This can be used on any kind of sequence, including tuples, lists and
    strings.
    '''
    from python_toolbox import nifty_collections
    big_sequence = ensure_iterable_is_sequence(big_sequence)
    small_sequence = ensure_iterable_is_sequence(small_sequence)
    small_sequence_length = len(small_sequence)
    last_index_that_subsequence_can_start = \
                                    len(big_sequence) - len(small_sequence) + 1
    matches = {}
    for i, item in enumerate(big_sequence):
        if matches:
            new_matches = {}
            for match_position, match_length in matches.items():
                if small_sequence[match_length] == item:
                    new_matches[match_position] = match_length + 1
            matches = new_matches
        if (item == small_sequence[0]) and \
                                   (i < last_index_that_subsequence_can_start):
            matches[i] = 1
        for match_position, match_length in matches.items():
            if match_length == small_sequence_length:
                return True


