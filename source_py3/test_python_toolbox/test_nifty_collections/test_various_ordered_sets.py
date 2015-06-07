# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox import emitting
from python_toolbox.nifty_collections import (OrderedSet, FrozenOrderedSet,
                                              EmittingOrderedSet)


class BaseOrderedSetTestCase(cute_testing.TestCase):
    __test__ = False
    
class BaseMutableOrderedSetTestCase(BaseOrderedSetTestCase):
    __test__ = False
    def test_sort(self):
        ordered_set = self.ordered_set_type([5, 61, 2, 7, 2])
        assert ordered_set != {5, 61, 2, 7}
        ordered_set.move_to_end(61)
        assert list(ordered_set) == [5, 2, 7, 61]
        ordered_set.sort()
        assert list(ordered_set) == [2, 5, 7, 61]
        ordered_set.sort(key=lambda x: -x, reverse=True)
        assert list(ordered_set) == [2, 5, 7, 61]
        
    def test_mutable(self):
        
        ordered_set = self.ordered_set_type(range(4))
        
        assert list(ordered_set) == list(range(4))
        assert len(ordered_set) == 4
        assert 1 in ordered_set
        assert 3 in ordered_set
        assert 7 not in ordered_set
        ordered_set.add(8)
        assert list(ordered_set)[-1] == 8
        ordered_set.discard(2)
        assert 2 not in ordered_set
        assert list(reversed(ordered_set)) == [8, 3, 1, 0]
        assert ordered_set.pop() == 8
        assert ordered_set.pop(last=False) == 0
        ordered_set.add(7, last=False)
        assert tuple(ordered_set) == (7, 1, 3)
        with cute_testing.RaiseAssertor(KeyError):
            ordered_set.remove('meow')
        ordered_set.discard('meow')
        ordered_set.discard('meow')
        ordered_set.discard('meow')
        
          

class OrderedSetTestCase(BaseMutableOrderedSetTestCase):
    __test__ = True
    ordered_set_type = OrderedSet

class FrozenOrderedSetTestCase(BaseOrderedSetTestCase):
    __test__ = True
    ordered_set_type = FrozenOrderedSet

    def test_frozen(self):
        
        frozen_ordered_set = self.ordered_set_type(range(4))
        
        assert list(frozen_ordered_set) == list(range(4))
        assert len(frozen_ordered_set) == 4
        assert 1 in frozen_ordered_set
        assert 3 in frozen_ordered_set
        assert 7 not in frozen_ordered_set
        with cute_testing.RaiseAssertor(AttributeError):
            frozen_ordered_set.add(8)
        with cute_testing.RaiseAssertor(AttributeError):
            frozen_ordered_set.discard(2)
        with cute_testing.RaiseAssertor(AttributeError):
            frozen_ordered_set.remove(2)
        with cute_testing.RaiseAssertor(AttributeError):
            frozen_ordered_set.clear()
        with cute_testing.RaiseAssertor(AttributeError):
            frozen_ordered_set.sort()
        with cute_testing.RaiseAssertor(AttributeError):
            frozen_ordered_set.move_to_end(2)
        with cute_testing.RaiseAssertor(AttributeError):
            frozen_ordered_set.pop(2)
        assert list(frozen_ordered_set) == list(range(4))
          


class EmittingOrderedSetTestCase(BaseMutableOrderedSetTestCase):
    __test__ = True
    ordered_set_type = EmittingOrderedSet
    def test_emitting(self):
        times_emitted = [0]
        def increment_times_emitted():
            times_emitted[0] += 1
        emitter = emitting.Emitter(outputs=increment_times_emitted)
        emitting_ordered_set = self.ordered_set_type(range(7), emitter=emitter)
        assert times_emitted == [0]
        emitting_ordered_set.add(7)
        assert times_emitted == [1]
        emitting_ordered_set.add(7)
        assert times_emitted == [1]
        emitting_ordered_set.discard(17)
        assert times_emitted == [1]
        assert emitting_ordered_set == OrderedSet(range(8))
        emitting_ordered_set |= (8, 9, 10)
        assert times_emitted == [4]
        emitting_ordered_set |= (8, 9, 10)
        assert times_emitted == [4]
        assert emitting_ordered_set == OrderedSet(range(11))
        emitting_ordered_set.move_to_end(4)
        assert times_emitted == [5]
        assert tuple(emitting_ordered_set) == \
                                             (0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 4)
        
        
        

        