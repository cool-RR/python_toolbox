# Copyright 2009-2015 Ram Rachum.
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


class UnorderedIterableException(Exception):
    '''
    An unordered iterable was encountered when we expected an orderable one.
    '''


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
    # If that ain't a damn clever implementation, I don't know what is. 
    iterator = iter(iterable)
    try:
        return sum(iterator, next(iterator))
    except StopIteration:
        return []


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
              range(0, enlarged_length, partition_size)]

    if fill_value != NO_FILL_VALUE and blocks:
        filler = itertools.repeat(fill_value,
                                  enlarged_length - sequence_length)
        blocks[-1].extend(filler)

    return blocks


def is_immutable_sequence(thing):
    '''Is `thing` an immutable sequence, like `tuple`?'''
    return isinstance(thing, collections.Sequence) and not \
                                 isinstance(thing, collections.MutableSequence)



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
        if isinstance(single_or_sequence, collections.Sequence):
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
    return {item: n_recurrences for item, n_recurrences in
            collections.Counter(sequence).most_common() if n_recurrences >= 2}

    
def ensure_iterable_is_immutable_sequence(iterable, default_type=tuple,
                                          unallowed_types=(),
                                          allow_unordered=True):
    '''
    Return a version of `iterable` that is an immutable sequence.
    
    If `iterable` is already an immutable sequence, it returns it as is;
    otherwise, it makes it into a `tuple`, or into any other data type
    specified in `default_type`.
    '''
    from python_toolbox import nifty_collections
    assert isinstance(iterable, collections.Iterable)
    if not allow_unordered and \
                   isinstance(iterable, nifty_collections.DefinitelyUnordered):
        raise UnorderedIterableException
    if isinstance(iterable, collections.MutableSequence) or \
       isinstance(iterable, unallowed_types) or \
       not isinstance(iterable, collections.Sequence):
        return default_type(iterable)
    else:
        return iterable


def ensure_iterable_is_sequence(iterable, default_type=tuple, 
                                unallowed_types=(bytes,), 
                                allow_unordered=True):
    '''
    Return a version of `iterable` that is a sequence.
    
    If `iterable` is already a sequence, it returns it as is; otherwise, it
    makes it into a `tuple`, or into any other data type specified in
    `default_type`.
    '''
    assert isinstance(iterable, collections.Iterable)
    if not allow_unordered and isinstance(iterable, (set, frozenset)):
        raise UnorderedIterableException
    if isinstance(iterable, collections.Sequence) and \
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
    
        
    
class CuteSequence(CuteSequenceMixin, collections.Sequence):
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
    