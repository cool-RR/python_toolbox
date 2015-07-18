# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `random_tools.shuffled`.'''

from python_toolbox import random_tools


def test():
    '''Test the basic workings of `shuffled`.'''
    my_range = range(50)
    shuffled_list = random_tools.shuffled(my_range)
    assert type(my_range) is type(shuffled_list) is list
    
    # The shuffled list has the same numbers...
    assert set(my_range) == set(shuffled_list)
    
    # ...But in a different order...
    assert my_range != shuffled_list
    
    # ...And the original list was not changed.
    assert my_range == list(range(50))
    
    # Immutable sequences work too:
    assert set(random_tools.shuffled((1, 2, 3))) == set((1, 2, 3))