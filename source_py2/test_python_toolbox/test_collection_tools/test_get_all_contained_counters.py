# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox import nifty_collections

from python_toolbox import collection_tools


def test():
    
    counter = collections.Counter('abracadabra')
    assert counter == collections.Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1,
                                           'd': 1,})
    all_contained_counters = \
                           collection_tools.get_all_contained_counters(counter)
    
    assert isinstance(all_contained_counters, nifty_collections.LazyTuple)
    
    assert not all_contained_counters.collected_data
    
    # Now we'll exhaust `all_contained_counters`:
    assert len(all_contained_counters) == 6 * 3 * 3 * 2 * 2
    assert all_contained_counters.exhausted
    
    assert counter in all_contained_counters
    assert collections.Counter({'a': 0, 'b': 0, 'r': 0, 'c': 0, 'd': 0,}) in \
                                                         all_contained_counters
    assert collections.Counter({'a': 1, 'b': 1, 'r': 1, 'c': 1, 'd': 1,}) in \
                                                         all_contained_counters
    assert collections.Counter({'a': 2, 'b': 2, 'r': 2, 'c': 1, 'd': 1,}) in \
                                                         all_contained_counters
    assert collections.Counter({'a': 4, 'b': 2, 'r': 2, 'c': 1, 'd': 1,}) in \
                                                         all_contained_counters
    assert all(isinstance(item, collections.Counter) for item in
                                                        all_contained_counters)