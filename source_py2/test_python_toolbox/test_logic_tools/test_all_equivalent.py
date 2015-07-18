# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import operator
import itertools

from python_toolbox.logic_tools import all_equivalent


def test():
    _check(False)
    _check(True)


def _check(assume_transitive):
    assert all_equivalent([1, 1, 1, 1], assume_transitive=assume_transitive)
    assert all_equivalent([1, 1, 1.0, 1], assume_transitive=assume_transitive)
    assert all_equivalent(((1 + 0j), 1, 1.0, 1),
                          assume_transitive=assume_transitive)
    assert all_equivalent([], assume_transitive=assume_transitive)
    assert all_equivalent(iter([1, 1, 1.0, 1]),
                          assume_transitive=assume_transitive)
    assert all_equivalent(set(('meow',)), assume_transitive=assume_transitive)
    assert all_equivalent(['frr', 'frr', 'frr', 'frr'],
                          assume_transitive=assume_transitive)
    
    assert not all_equivalent([1, 1, 2, 1],
                              assume_transitive=assume_transitive)
    assert not all_equivalent([1, 1, 1.001, 1],
                              assume_transitive=assume_transitive)
    assert not all_equivalent(((1 + 0j), 3, 1.0, 1),
                              assume_transitive=assume_transitive)
    assert not all_equivalent(range(7), assume_transitive=assume_transitive)
    assert not all_equivalent(iter([1, 17, 1.0, 1]),
                              assume_transitive=assume_transitive)
    assert not all_equivalent(set(('meow', 'grr')),
                              assume_transitive=assume_transitive)
    assert not all_equivalent(['frr', 'frr', {}, 'frr', 'frr'],
                              assume_transitive=assume_transitive)
    assert not all_equivalent(itertools.count())
    # Not using given `assume_transitive` flag here because `count()` is
    # infinite.
    
    
def test_assume_transitive_false():
    '''
    Test `all_equivalent` in cases where `assume_transitive=False` is relevant.
    '''
    
    class FunkyFloat(float):
        def __eq__(self, other):
            return (abs(self - other) <= 2)
        
    funky_floats = [
        FunkyFloat(1),
        FunkyFloat(2),
        FunkyFloat(3),
        FunkyFloat(4)
    ]
    
    assert all_equivalent(funky_floats)
    assert not all_equivalent(funky_floats, assume_transitive=False)
    
    
def test_all_assumptions():
    class EquivalenceChecker:
        pairs_checked = []
        def __init__(self, tag):
            self.tag = tag
        def is_equivalent(self, other):
            EquivalenceChecker.pairs_checked.append((self, other))
            return True
        def __eq__(self, other):
            return (type(self), self.tag) == (type(other), other.tag)
            
    def get_pairs_for_options(**kwargs):
        assert EquivalenceChecker.pairs_checked == []
        # Testing with an iterator instead of the tuple to ensure it works and that
        # the function doesn't try to exhaust it twice.
        assert all_equivalent(iter(things), EquivalenceChecker.is_equivalent,
                              **kwargs) is True
        try:
            return tuple((a.tag, b.tag) for (a, b) in
                         EquivalenceChecker.pairs_checked)
        finally:
            EquivalenceChecker.pairs_checked = []
        
    x0 = EquivalenceChecker(0)
    x1 = EquivalenceChecker(1)
    x2 = EquivalenceChecker(2)
    things = (x0, x1, x2)
    
    assert get_pairs_for_options(assume_reflexive=False, assume_symmetric=False,
                                 assume_transitive=False) == (
        (0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1), (0, 0), (1, 1), (2, 2)
    )
    assert get_pairs_for_options(assume_reflexive=False, assume_symmetric=False,
                                 assume_transitive=True) == (
        (0, 1), (1, 0), (1, 2), (2, 1), (0, 0), (1, 1), (2, 2)
    )
    assert get_pairs_for_options(assume_reflexive=False, assume_symmetric=True,
                                 assume_transitive=False) == (
        (0, 1), (0, 2), (1, 2), (0, 0), (1, 1), (2, 2)
    )
    assert get_pairs_for_options(assume_reflexive=False, assume_symmetric=True,
                                 assume_transitive=True) == (
        (0, 1), (1, 2), (0, 0), (1, 1), (2, 2)
    )
    assert get_pairs_for_options(assume_reflexive=True, assume_symmetric=False,
                                 assume_transitive=False) == (
        (0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1),
    )
    assert get_pairs_for_options(assume_reflexive=True, assume_symmetric=False,
                                 assume_transitive=True) == (
        (0, 1), (1, 0), (1, 2), (2, 1),
    )
    assert get_pairs_for_options(assume_reflexive=True, assume_symmetric=True,
                                 assume_transitive=False) == (
        (0, 1), (0, 2), (1, 2),
    )
    assert get_pairs_for_options(assume_reflexive=True, assume_symmetric=True,
                                 assume_transitive=True) == ((0, 1), (1, 2))
    
                
    
    
def test_custom_relations():
    assert all_equivalent(range(4), relation=operator.ne) is True
    assert all_equivalent(range(4), relation=operator.ge) is False
    assert all_equivalent(range(4), relation=operator.le) is True
    assert all_equivalent(range(4), relation=operator.le,
                          assume_transitive=True) is True
    # (Always comparing small to big, even on `assume_transitive=False`.)
    
    assert all_equivalent(range(4),
                          relation=lambda x, y: (x // 10 == y // 10)) is True
    assert all_equivalent(range(4),
                          relation=lambda x, y: (x // 10 == y // 10),
                          assume_transitive=True) is True
    assert all_equivalent(range(8, 12), 
                          relation=lambda x, y: (x // 10 == y // 10)) is False
    assert all_equivalent(range(8, 12),
                          relation=lambda x, y: (x // 10 == y // 10),
                          assume_transitive=True) is False
    