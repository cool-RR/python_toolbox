# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `random_tools.shuffled`.'''

from garlicsim.general_misc import random_tools


def test():
    '''Test the basic workings of `shuffled`.'''
    my_range = range(30)
    shuffled_list = random_tools.shuffled(my_range)
    assert type(my_range) is type(shuffled_list) is list
    
    # The shuffled list has the same numbers...
    assert set(my_range) == set(shuffled_list)
    
    # ...But in a different order...
    assert my_range != shuffled_list
    
    # ...And the original list was not changed.
    assert my_range == range(30)