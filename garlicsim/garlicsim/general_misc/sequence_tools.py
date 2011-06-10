# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for manipulating sequences.'''

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
    # blocktodo: test
    # blocktododoc arguments
    
    sequence_length = len(sequence)
    
    ### Validating input: #####################################################
    #                                                                         #
    if (partition_size is None) == (n_partitions is None):
        raise Exception('You must specify *either* `partition_size` *or* '
                        '`n_paritions`.')
    
    remainder_length = sequence_length % (partition_size if partition_size
                                          is not None else n_partitions)

    if not allow_remainder and remainder_length > 0:
        raise Exception("You set `allow_reminder=False`, but there's a "
                        "reminder of %s left." % \
                        (len(sequence) % partition_size))
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
    return abcs_collection.Sequence.__instancecheck__(thing)


def is_mutable_sequence(thing):
    return abcs_collection.MutableSequence.__instancecheck__(thing)


def is_immutable_sequence(thing):
    return abcs_collection.Sequence.__instancecheck__(thing) and not \
           abcs_collection.MutableSequence.__instancecheck__(thing)


def parse_slice(s):
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
            stop = 0
    ###
            
    return (start, stop, step)

    
    
### Not using now, might want in future:

#def heads(sequence, include_empty=False, include_full=True):    
    #for i in range(0 if include_empty else 1, len(sequence)):
        #yield sequence[:i]
    #if include_full:
        #yield sequence[:]