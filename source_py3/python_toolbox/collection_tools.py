# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to data structures.'''

import collections
import itertools
import numbers

from python_toolbox import nifty_collections


@nifty_collections.LazyTuple.factory
def get_all_contained_counters(counter):
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
