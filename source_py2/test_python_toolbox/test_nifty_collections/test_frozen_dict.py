# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import uuid
import pickle
import itertools
import collections

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import FrozenDict


def test():
    frozen_dict = FrozenDict({'1': 'a', '2': 'b', '3': 'c',})
    assert len(frozen_dict) == 3
    assert set(frozen_dict) == set(frozen_dict.keys()) == set('123')
    assert set(frozen_dict.values()) == set('abc')
    assert set(frozen_dict.items()) == {('1', 'a'), ('2', 'b'), ('3', 'c'),}
    assert frozen_dict['1'] == 'a'
    with cute_testing.RaiseAssertor(exception_type=LookupError):
        frozen_dict['missing value']
    assert {frozen_dict, frozen_dict} == {frozen_dict}
    assert {frozen_dict: frozen_dict} == {frozen_dict: frozen_dict}
    assert isinstance(hash(frozen_dict), int)
    
    assert frozen_dict.copy({'meow': 'frrr'}) == \
           frozen_dict.copy(meow='frrr') == \
           FrozenDict({'1': 'a', '2': 'b', '3': 'c', 'meow': 'frrr',})
    
    assert repr(frozen_dict).startswith('FrozenDict(')
    
    assert pickle.loads(pickle.dumps(frozen_dict)) == frozen_dict