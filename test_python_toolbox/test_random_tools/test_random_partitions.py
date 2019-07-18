# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing package for `python_toolbox.random_tools`.'''

from python_toolbox import random_tools
from python_toolbox import sequence_tools


def test():
    '''Test the basic workings of `random_partitions`.'''

    def assert_correct_members(partitions):
        '''
        Assert that the `partitions` contain exactly all of `r`'s members.
        '''
        members = sequence_tools.flatten(partitions)
        assert len(members) == len(r)
        assert set(members) == set(r)

    r = list(range(10))

    for partition_size in range(1, len(r)):
        partitions = random_tools.random_partitions(r, partition_size)
        for partition in partitions[:-1]:
            assert len(partition) == partition_size
        assert len(partitions[-1]) <= partition_size
        assert_correct_members(partitions)

    for n_partitions in range(1, len(r)):
        partitions = random_tools.random_partitions(r,
                                                    n_partitions=n_partitions)
        assert len(partitions) == n_partitions
        assert_correct_members(partitions)


