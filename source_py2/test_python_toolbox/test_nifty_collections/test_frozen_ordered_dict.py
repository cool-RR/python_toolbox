# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import uuid
import pickle
import itertools
import collections

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import FrozenOrderedDict


def test():
    frozen_ordered_dict = \
                        FrozenOrderedDict((('1', 'a'), ('2', 'b'), ('3', 'c')))
    assert len(frozen_ordered_dict) == 3
    assert set(frozen_ordered_dict) == set(frozen_ordered_dict.keys()) == \
                                                                     set('123')
    assert set(frozen_ordered_dict.values()) == set('abc')
    assert set(frozen_ordered_dict.items()) == \
                                     set((('1', 'a'), ('2', 'b'), ('3', 'c'),))
    assert frozen_ordered_dict['1'] == 'a'
    with cute_testing.RaiseAssertor(exception_type=LookupError):
        frozen_ordered_dict['missing value']
    assert set((frozen_ordered_dict, frozen_ordered_dict)) == \
                                                    set((frozen_ordered_dict,))
    assert {frozen_ordered_dict: frozen_ordered_dict} == \
                                     {frozen_ordered_dict: frozen_ordered_dict}
    assert isinstance(hash(frozen_ordered_dict), int)
    
    assert frozen_ordered_dict.copy({'meow': 'frrr'}) == \
           frozen_ordered_dict.copy(meow='frrr') == \
           FrozenOrderedDict((('1', 'a'), ('2', 'b'), ('3', 'c'),
                              ('meow', 'frrr')))
    
    assert repr(frozen_ordered_dict).startswith('FrozenOrderedDict(')
    
    assert pickle.loads(pickle.dumps(frozen_ordered_dict)) == \
                                                            frozen_ordered_dict    
def test_reversed():

    frozen_ordered_dict = \
                        FrozenOrderedDict((('1', 'a'), ('2', 'b'), ('3', 'c')))
    
    assert frozen_ordered_dict.reversed == \
                        FrozenOrderedDict((('3', 'c'), ('2', 'b'), ('1', 'a')))
    
    assert frozen_ordered_dict.reversed is frozen_ordered_dict.reversed
    assert frozen_ordered_dict.reversed == frozen_ordered_dict.reversed
    assert frozen_ordered_dict.reversed.reversed is \
                                          frozen_ordered_dict.reversed.reversed
    assert frozen_ordered_dict.reversed.reversed == \
                                          frozen_ordered_dict.reversed.reversed
    assert frozen_ordered_dict.reversed.reversed == frozen_ordered_dict
    assert frozen_ordered_dict.reversed.reversed.reversed == \
                                                   frozen_ordered_dict.reversed
    
    assert set(frozen_ordered_dict.items()) == \
                                      set(frozen_ordered_dict.reversed.items())
    assert tuple(frozen_ordered_dict.items()) == \
                   tuple(reversed(tuple(frozen_ordered_dict.reversed.items())))
    assert type(frozen_ordered_dict.reversed) is type(frozen_ordered_dict) \
                                                           is FrozenOrderedDict
