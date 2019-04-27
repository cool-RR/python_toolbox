# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for creating randomness.'''

import random

from python_toolbox import sequence_tools


def random_partitions(sequence, partition_size=None, n_partitions=None,
                      allow_remainder=True):
    '''
    Randomly partition `sequence` into partitions of size `partition_size`.

    If the sequence can't be divided into precisely equal partitions, the last
    partition will contain less members than all the other partitions.

    Example:

        >>> random_partitions([0, 1, 2, 3, 4], 2)
        [[0, 2], [1, 4], [3]]

    (You need to give *either* a `partition_size` *or* an `n_partitions`
    argument, not both.)

    Specify `allow_remainder=False` to enforce that the all the partition sizes
    be equal; if there's a remainder while `allow_remainder=False`, an
    exception will be raised.
    '''

    shuffled_sequence = shuffled(sequence)

    return sequence_tools.partitions(
        shuffled_sequence, partition_size=partition_size,
        n_partitions=n_partitions, allow_remainder=allow_remainder
    )


def shuffled(sequence):
    '''
    Return a list with all the items from `sequence` shuffled.

    Example:

        >>> random_tools.shuffled([0, 1, 2, 3, 4, 5])
        [0, 3, 5, 1, 4, 2]

    '''
    sequence_copy = list(sequence)
    random.shuffle(sequence_copy)
    return sequence_copy