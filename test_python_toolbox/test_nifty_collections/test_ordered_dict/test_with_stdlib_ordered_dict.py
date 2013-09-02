# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import sys

from python_toolbox import cute_testing

from python_toolbox.nifty_collections.ordered_dict import OrderedDict
from collections import OrderedDict as StdlibOrderedDict


def test():
    if sys.version_info[:2] <= (2, 6):
        raise nose.SkipTest
    
    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    stdlib_ordered_dict = StdlibOrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    
    assert ordered_dict == stdlib_ordered_dict
    assert stdlib_ordered_dict == ordered_dict
    assert ordered_dict.items() == stdlib_ordered_dict.items()
    assert ordered_dict.keys() == stdlib_ordered_dict.keys()
    assert ordered_dict.values() == stdlib_ordered_dict.values()
    
    ordered_dict.move_to_end(1)
    
    assert ordered_dict != stdlib_ordered_dict
    assert stdlib_ordered_dict != ordered_dict
    assert ordered_dict.items() != stdlib_ordered_dict.items()
    assert ordered_dict.keys() != stdlib_ordered_dict.keys()
    assert ordered_dict.values() != stdlib_ordered_dict.values()
    
    stdlib_ordered_dict.move_to_end(1)
    
    assert ordered_dict == stdlib_ordered_dict
    assert stdlib_ordered_dict == ordered_dict
    assert ordered_dict.items() == stdlib_ordered_dict.items()
    assert ordered_dict.keys() == stdlib_ordered_dict.keys()
    assert ordered_dict.values() == stdlib_ordered_dict.values()
    
    assert ordered_dict == OrderedDict(stdlib_ordered_dict) == \
                                                            stdlib_ordered_dict
    assert ordered_dict == StdlibOrderedDict(ordered_dict) == \
                                                            stdlib_ordered_dict
    