# Copyright 2009-2014 Ram Rachum.
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
from python_toolbox import cute_iter_tools

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
                     in range(1, length + 1))
        yield from itertools.chain(*iterators)

    elif n == 1:
        for thing in itertools.islice(sequence, start, None):
            yield [thing]
    else:
        assert n > 1
        for (i, thing) in itertools.islice(enumerate(sequence), start, None):
            for sub_result in combinations(sequence, n - 1, start=(i + 1)):
                yield [thing] + sub_result


class NO_FILL_VALUE:
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
                                          unallowed_types=(bytes,),
                                          allow_unordered=True):
    '''
    Return a version of `iterable` that is an immutable sequence.
    
    If `iterable` is already an immutable sequence, it returns it as is;
    otherwise, it makes it into a `tuple`, or into any other data type
    specified in `default_type`.
    '''
    assert isinstance(iterable, collections.Iterable)
    if not allow_unordered and isinstance(iterable, (set, frozenset)):
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


class CanonicalSlice:
    def __init__(self, slice_, iterable_or_length=None, offset=0):
        '''
        blocktododoc iterable_or_length, also note result, if not given iterable/length, can't really be used as slice (only as canonical object) because of `infinity`
        
        Parse a `slice` object into a canonical `(start, stop, step)`.
    
        This is helpful because `slice`'s own `.start`, `.stop` and `.step` are
        sometimes specified as `None` for convenience, so Python will infer
        them automatically. Here we make them explicit.
    
        if `start` is `None`, it will be set to `0` (if the `step` is positive)
        or `infinity` (if the `step` is negative.)
    
        if `stop` is `None`, it will be set to `infinity` (if the `step` is
        positive) or `0` (if the `step` is negative.)
    
        If `step` is `None`, it will be changed to the default `1`.
        '''
        from . import math_tools
        
        if isinstance(slice_, CanonicalSlice):
            slice_ = slice(slice_.start, slice_.stop, slice_.step)
        assert isinstance(slice_, slice)
        self.given_slice = slice_
        if iterable_or_length is not None:
            if isinstance(iterable_or_length,
                          math_tools.PossiblyInfiniteIntegral):
                self.length = iterable_or_length
            elif isinstance(iterable_or_length, collections.Sequence):
                self.length = get_length(iterable_or_length)
            else:
                assert isinstance(iterable_or_length, collections.Iterable)
                self.length = cute_iter_tools.get_length(iterable)
        else:
            self.length = None
            
        self.offset = offset
            
        ### Parsing `step`: ###################################################
        #                                                                     #
        assert slice_.step != 0
        if slice_.step is None:
            self.step = 1
        else:
            self.step = slice_.step
        #                                                                     #
        ### Finished parsing `step`. ##########################################

            
        ### Parsing `start`: #################################################
        #                                                                    #
        if slice_.start is None:
            if self.step > 0:
                self.start = 0 + self.offset
            else:
                assert self.step < 0
                self.start = (self.length + self.offset) if \
                                        (self.length is not None) else infinity
        else: # s.start is not None
            if self.length is not None:
                if slice_.start < 0:
                    self.start = \
                               max(slice_.start + self.length, 0) + self.offset
                else:
                    self.start = min(slice_.start, self.length) + self.offset
            else: 
                self.start = slice_.start + self.offset
        #                                                                     #
        ### Finished parsing `start`. #########################################
        
        ### Parsing `stop`: ###################################################
        #                                                                     #
        if slice_.stop is None:
            if self.step > 0:
                self.stop = (self.length + self.offset) if \
                                        (self.length is not None) else infinity
            else:
                assert self.step < 0
                self.stop = -infinity 
            
        else: # slice_.stop is not None
            if self.length is not None:
                if slice_.stop < 0:
                    self.stop = max(slice_.stop + self.length, 0) + self.offset
                else: # slice_.stop >= 0
                    self.stop = min(slice_.stop, self.length) + self.offset
            else: 
                self.stop = slice_.stop + self.offset 
        #                                                                     #
        ### Finished parsing `stop`. ##########################################
            
        if (self.step > 0 and self.start >= self.stop > 0) or \
           (self.step < 0 and self.stop >= self.start):
            # We have a case of an empty slice.
            self.start = self.stop = 0
        
            
        self.slice_ = slice(*((item if item not in math_tools.infinities
                               else None) for item in self))
            
        ### Doing sanity checks: ##############################################
        #                                                                     #
        if self.length:
            if self.step > 0:
                assert 0 <= self.start <= \
                                         self.stop <= self.length + self.offset
            else:
                assert self.step < 0
                assert 0 <= self.stop <= \
                                        self.start <= self.length + self.offset
        #                                                                     #
        ### Finished doing sanity checks. #####################################
        
    __iter__ = lambda self: iter((self.start, self.stop, self.step))
    __repr__ = lambda self: '%s%s' % (type(self).__name__, tuple(self))
    _reduced = property(lambda self: (type(self), tuple(self)))
    __hash__ = lambda self: hash(self._reduced)
    __eq__ = lambda self, other: (isinstance(other, CanonicalSlice) and
                                  self._reduced == other._reduced)
    __contains__ = lambda self, number: self.start <= number < self.stop
    
    
    
class CuteSequenceMixin(misc_tools.AlternativeLengthMixin):
    def take_random(self):
        return self[random.randint(0, get_length(self))]
    def __contains__(self, item):
        try: self.index(item)
        except ValueError: return False
        else: return True
    
        
    
class CuteSequence(CuteSequenceMixin, collections.Sequence):
    pass


def get_length(sequence):
    return sequence.length if hasattr(sequence, 'length') else len(sequence)
        
        
def divide_to_slices(sequence, n_slices):
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