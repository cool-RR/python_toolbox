# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing package for `garlicsim.general_misc.random_tools`.'''


from garlicsim.general_misc import random_tools
from garlicsim.general_misc import sequence_tools


def test():
    def assert_correct_members(partitions):
        members = sequence_tools.flatten(partitions)
        assert len(members) == len(r)
        assert set(members) == set(r)
        
    r = range(10)
    
    for partition_size in range(len(r)):
        partitions = random_tools.random_partitions(r, partition_size)
        for partition in partitions:
            assert len(partition) == partition_size
        assert_correct_members(partitions)
        
        
    for n_partitions in range(len(r)):
        partitions = random_tools.random_partitions(r, n_partitions)
        for partition in partitions:
            assert len(partition) == partition_size
        assert_correct_members(partitions)
        
        
        