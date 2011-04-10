# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for creating randomness.'''

import random


def random_partition(sequence, partition_size, allow_reminder=False):
    '''
    Randomly partition `sequence` into partitions of size `partition_size`.
    
    Example:
    
        >>> random_partition([0, 1, 2, 3, 4, 5], 2)
        [(0, 2), (1, 4), (3, 5)]
    
    '''
    if allow_reminder:
        raise NotImplementedError
    if len(sequence) % partition_size != 0:
        raise Exception("You set `allow_reminder=False`, but there's a "
                        "reminder of %s left." % \
                        (len(sequence) % partition_size))
    
    shuffled_sequence = shuffled(sequence)

    subsequences = [shuffled_sequence[i::partition_size] for i in
                    xrange(partition_size)]
    
    return zip(*subsequences)


def shuffled(sequence):
    '''
    Return a list with all the items from `sequence` shuffled.
    
    Example:
    
        >>> random_tools.shuffled([0, 1, 2, 3, 4, 5])
        [0, 3, 5, 1, 4, 2]
        
    '''
    sequence_copy = sequence[:]
    random.shuffle(sequence_copy)
    return sequence_copy