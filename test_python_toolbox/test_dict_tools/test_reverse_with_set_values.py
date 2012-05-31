# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''Test package for `dict_tools.reverse_with_set_values`.'''

from python_toolbox import dict_tools


def test():
    '''Test the basic workings of `reverse_with_set_values`.'''
    assert dict_tools.reverse_with_set_values({1: 2, 3: 4, 'meow': 2}) == \
                                             {2: set([1, 'meow']), 4: set([3])}