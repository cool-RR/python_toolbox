# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for manipulating sequences.'''

import types
import itertools

from garlicsim.general_misc.nifty_collections import Counter
from garlicsim.general_misc import caching
from garlicsim.general_misc import math_tools
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc.third_party import abcs_collection

        
def are_equal_regardless_of_order(seq1, seq2):
    '''
    Return whether the two sequences are equal in the elements they contain,
    regardless of the order of the elements.
    
    Currently will fail for items that have problems with comparing.
    '''
    return Counter(seq1) == Counter(seq2)
        

def flatten(iterable):
    '''
    Flatten a sequence, returning a sequence of all its items' items.
    
    For example, `flatten([[1, 2], [3], [4, 'meow']]) == [1, 2, 3, 4, 'meow']`.
    '''
    
    iterator = iter(iterable)
    try:
        first_item = iterator.next()
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

                
def partitions(sequence, partition_size=None, n_partitions=None,
               allow_remainder=True):
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
    '''
    
    sequence_length = len(sequence)
    
    ### Validating input: #####################################################
    #                                                                         #
    if (partition_size is None) == (n_partitions is None):
        raise Exception('You must specify *either* `partition_size` *or* '
                        '`n_paritions`.')
    
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
    
    return blocks
    
                
                
def is_sequence(thing):
    '''Is `thing` a sequence, like `list` or `tuple`?'''
    return abcs_collection.Sequence.__instancecheck__(thing)


def is_mutable_sequence(thing):
    '''Is `thing` a mutable sequence, like `list`?'''
    return abcs_collection.MutableSequence.__instancecheck__(thing)


def is_immutable_sequence(thing):
    '''Is `thing` an immutable sequence, like `tuple`?'''
    return abcs_collection.Sequence.__instancecheck__(thing) and not \
           abcs_collection.MutableSequence.__instancecheck__(thing)


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
    
        
def pop_until(sequence, condition=None):
    '''
    Propagates whatever error is raised on popping the sequence.
    '''
    condition = condition or bool
    while True:
        item = sequence.pop()
        if condition(item):
            return item
        
    
    
### Not using now, might want in future:

#def heads(sequence, include_empty=False, include_full=True):    
    #for i in range(0 if include_empty else 1, len(sequence)):
        #yield sequence[:i]
    #if include_full:
        #yield sequence[:]