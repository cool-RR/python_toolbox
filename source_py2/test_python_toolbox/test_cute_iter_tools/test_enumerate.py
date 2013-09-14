# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.enumerate`.'''

from python_toolbox import cute_iter_tools


def test():
    '''Test the basic workings of `cute_iter_tools.enumerate`.'''
    
    for i, j in cute_iter_tools.enumerate(range(5)):
        assert i == j
        
    for i, j in cute_iter_tools.enumerate(range(5), reverse_index=True):
        assert i + j == 4
        
    for i, j in cute_iter_tools.enumerate(range(5, 0 -1), reverse_index=True):
        assert i == j
        
    
