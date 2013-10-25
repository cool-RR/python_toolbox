# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.nifty_collections.LazyTuple`.'''

import uuid
import itertools
import collections

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import FrozenCounter


def test():
    frozen_counter = FrozenCounter('abracadabra')
    assert frozen_counter == collections.Counter('abracadabra') == \
           collections.Counter(frozen_counter) == \
           FrozenCounter(collections.Counter('abracadabra'))
    
    assert len(frozen_counter) == 5
    assert set(frozen_counter) == set(frozen_counter.keys()) == \
                                                             set('abracadabra')
    assert set(frozen_counter.values()) == {1, 2, 5}
    assert set(frozen_counter.items()) == \
                             {('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)}
    assert frozen_counter['a'] == 5
    assert frozen_counter['missing value'] == 0
    assert len(frozen_counter) == 5
    assert {frozen_counter, frozen_counter} == {frozen_counter}
    assert {frozen_counter: frozen_counter} == {frozen_counter: frozen_counter}
    assert isinstance(hash(frozen_counter), int)
    
    assert frozen_counter.copy({'meow': 9}) == \
           frozen_counter.copy(meow=9) == \
           FrozenCounter({'a': 5, 'r': 2, 'b': 2, 'c': 1, 'd': 1,
                          'meow': 9,})
    
    assert set(frozen_counter.most_common()) == \
                         set(collections.Counter(frozen_counter).most_common())
    
    assert frozen_counter + frozen_counter == FrozenCounter('abracadabra'*2)
    assert frozen_counter - frozen_counter == FrozenCounter()
    assert frozen_counter - FrozenCounter('a') == FrozenCounter('abracadabr')
    assert frozen_counter - FrozenCounter('a') == FrozenCounter('abracadabr')
    assert frozen_counter | FrozenCounter('a') == frozen_counter
    assert frozen_counter | frozen_counter == \
           frozen_counter | frozen_counter | frozen_counter == \
                                                                 frozen_counter
    assert frozen_counter & FrozenCounter('a') == FrozenCounter('a')
    assert frozen_counter & frozen_counter == \
           frozen_counter & frozen_counter & frozen_counter == \
                                                                 frozen_counter
    
    assert FrozenCounter(frozen_counter.elements()) == frozen_counter
    
    assert +frozen_counter == frozen_counter
    assert ---frozen_counter == -frozen_counter != \
                                             frozen_counter == --frozen_counter
    
    assert repr(frozen_counter).startswith('FrozenCounter(')