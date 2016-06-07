# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import sys

import nose

from python_toolbox import cute_testing

from python_toolbox.nifty_collections.ordered_dict import OrderedDict
from python_toolbox.nifty_collections.ordered_dict import StdlibOrderedDict


def test():

    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    stdlib_ordered_dict = StdlibOrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    
    assert ordered_dict == stdlib_ordered_dict
    assert stdlib_ordered_dict == ordered_dict
    assert ordered_dict.items() == stdlib_ordered_dict.items()
    assert ordered_dict.keys() == stdlib_ordered_dict.keys()
    assert ordered_dict.values() == stdlib_ordered_dict.values()
    
    ordered_dict.move_to_end(1)
    
    assert ordered_dict != stdlib_ordered_dict
    #assert stdlib_ordered_dict != ordered_dict
    assert ordered_dict.items() != stdlib_ordered_dict.items()
    assert ordered_dict.keys() != stdlib_ordered_dict.keys()
    assert ordered_dict.values() != stdlib_ordered_dict.values()
    
    del stdlib_ordered_dict[1]
    stdlib_ordered_dict[1] = 'a'
    
    assert ordered_dict == stdlib_ordered_dict
    assert stdlib_ordered_dict == ordered_dict
    assert ordered_dict.items() == stdlib_ordered_dict.items()
    assert ordered_dict.keys() == stdlib_ordered_dict.keys()
    assert ordered_dict.values() == stdlib_ordered_dict.values()
    
    assert ordered_dict == OrderedDict(stdlib_ordered_dict) == \
                                                            stdlib_ordered_dict
    assert ordered_dict == StdlibOrderedDict(ordered_dict) == \
                                                            stdlib_ordered_dict
    