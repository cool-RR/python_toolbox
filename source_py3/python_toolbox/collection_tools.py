# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to data structures.'''

import collections
import itertools
import numbers

from python_toolbox import nifty_collections


@nifty_collections.LazyTuple.factory
def get_all_contained_counters(counter, use_lazy_tuple=True):
    '''
    Get all counters that are subsets of `counter`.
    
    This means all counters that have amounts identical or smaller than
    `counter` for each of its keys.
    
    If `use_lazy_tuple=True` (default), value is returned as a `LazyTuple`, so
    it may be used both by lazily iterating on it *and* as a tuple. Otherwise
    an iterator is returned.
    '''
    iterator = _get_all_contained_counters(counter)
    if use_lazy_tuple:
        return nifty_collections.LazyTuple(iterator)
    else:
        return iterator
        

def _get_all_contained_counters(counter, use_lazy_tuple=True):
    assert isinstance(counter, collections.Counter)
    counter_type = type(counter)
    keys, amounts = zip(
        *((key, amount) for key, amount in counter.items() if amount)
    )
    assert all(isinstance(amount, numbers.Integral) for amount in amounts)
    amounts_tuples = \
               itertools.product(*map(lambda amount: range(amount+1), amounts))
    for amounts_tuple in amounts_tuples:
        yield counter_type(dict(zip(keys, amounts_tuple)))
