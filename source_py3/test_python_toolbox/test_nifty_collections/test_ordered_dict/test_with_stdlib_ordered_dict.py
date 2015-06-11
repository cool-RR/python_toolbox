# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import sys

import nose

from python_toolbox import cute_testing

from python_toolbox.nifty_collections.ordered_dict import OrderedDict


def test():
    from collections import OrderedDict as StdlibOrderedDict

    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    stdlib_ordered_dict = StdlibOrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    
    assert ordered_dict == stdlib_ordered_dict
    assert stdlib_ordered_dict == ordered_dict
    assert list(ordered_dict.items()) == list(stdlib_ordered_dict.items())
    assert list(ordered_dict.keys()) == list(stdlib_ordered_dict.keys())
    assert list(ordered_dict.values()) == list(stdlib_ordered_dict.values())
    
    ordered_dict.move_to_end(1)
    
    assert ordered_dict != stdlib_ordered_dict
    #assert stdlib_ordered_dict != ordered_dict
    assert list(ordered_dict.items()) != list(stdlib_ordered_dict.items())
    assert list(ordered_dict.keys()) != list(stdlib_ordered_dict.keys())
    assert list(ordered_dict.values()) != list(stdlib_ordered_dict.values())
    
    del stdlib_ordered_dict[1]
    stdlib_ordered_dict[1] = 'a'
    
    assert ordered_dict == stdlib_ordered_dict
    assert stdlib_ordered_dict == ordered_dict
    assert list(ordered_dict.items()) == list(stdlib_ordered_dict.items())
    assert list(ordered_dict.keys()) == list(stdlib_ordered_dict.keys())
    assert list(ordered_dict.values()) == list(stdlib_ordered_dict.values())
    
    assert ordered_dict == OrderedDict(stdlib_ordered_dict) == \
                                                            stdlib_ordered_dict
    assert ordered_dict == StdlibOrderedDict(ordered_dict) == \
                                                            stdlib_ordered_dict
    