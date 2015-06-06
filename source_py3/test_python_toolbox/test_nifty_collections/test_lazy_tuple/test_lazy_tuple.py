# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.nifty_collections.LazyTuple`.'''

import uuid
import itertools
import collections

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import LazyTuple


class SelfAwareUuidIterator(collections.Iterator):
    '''Iterator that gives UUIDs and keeps them all in an internal list.'''
    def __init__(self):
        self.data = []
    def __next__(self):
        new_entry = uuid.uuid4()
        self.data.append(new_entry)
        return new_entry

    
def test():
    '''Test the basic workings of `LazyTuple`.'''    
    self_aware_uuid_iterator = SelfAwareUuidIterator()
    lazy_tuple = LazyTuple(self_aware_uuid_iterator)
    assert len(self_aware_uuid_iterator.data) == 0
    assert not lazy_tuple.is_exhausted
    assert repr(lazy_tuple) == '<LazyTuple: (...)>'
    
    first = lazy_tuple[0]
    assert len(self_aware_uuid_iterator.data) == 1
    assert isinstance(first, uuid.UUID)
    assert first == self_aware_uuid_iterator.data[0]
    
    first_ten = lazy_tuple[:10]
    assert isinstance(first_ten, tuple)
    assert len(self_aware_uuid_iterator.data) == 10
    assert first_ten[0] == first
    assert all(isinstance(item, uuid.UUID) for item in first_ten)
    
    weird_slice = lazy_tuple[15:5:-3]
    assert isinstance(first_ten, tuple)
    assert len(self_aware_uuid_iterator.data) == 16
    assert len(weird_slice) == 4
    assert weird_slice[2] == first_ten[-1] == lazy_tuple[9]
    assert not lazy_tuple.is_exhausted
    
    iterator_twenty = cute_iter_tools.shorten(lazy_tuple, 20)
    assert len(self_aware_uuid_iterator.data) == 16
    first_twenty = list(iterator_twenty)
    assert len(self_aware_uuid_iterator.data) == 20
    assert len(first_twenty) == 20
    assert first_twenty[:10] == list(first_ten)
    assert first_twenty == self_aware_uuid_iterator.data
    
    iterator_twelve = cute_iter_tools.shorten(lazy_tuple, 12)
    first_twelve = list(iterator_twelve)
    assert len(self_aware_uuid_iterator.data) == 20
    assert len(first_twelve) == 12
    assert first_twenty[:12] == first_twelve
    
    assert bool(lazy_tuple) == True
    

def test_empty():
    '''Test an empty `LazyTuple`.'''
    def empty_generator():
        if False: yield # (Unreachable `yield` to make this a generator.)
        return
    lazy_tuple = LazyTuple(empty_generator())
    assert repr(lazy_tuple) == '<LazyTuple: (...)>'
    
    with cute_testing.RaiseAssertor(IndexError):
        lazy_tuple[7]
        
    assert repr(lazy_tuple) == '<LazyTuple: []>'
    
    assert bool(LazyTuple(())) == False
    assert bool(lazy_tuple) == False
        
    
    
def test_string():
    '''Test a `LazyTuple` built from a string.'''
    string = 'meow'
    lazy_tuple = LazyTuple(string)
    assert lazy_tuple.is_exhausted
    assert repr(lazy_tuple) == "<LazyTuple: 'meow'>"
    assert ''.join(lazy_tuple) == string
    assert ''.join(lazy_tuple[1:-1]) == string[1:-1]
    
    assert len(lazy_tuple) == lazy_tuple.known_length == \
           len(lazy_tuple.collected_data)
    
    assert LazyTuple(reversed(LazyTuple(reversed(lazy_tuple)))) == lazy_tuple
    
    
def test_infinite():
    '''Test an infinite `LazyTuple`.'''
    lazy_tuple = LazyTuple(itertools.count())
    assert not lazy_tuple.is_exhausted
    lazy_tuple[100]
    assert len(lazy_tuple.collected_data) == 101
    assert not lazy_tuple.is_exhausted
    

def test_factory_decorator():
    '''Test the `LazyTuple.factory` decorator.'''
    @LazyTuple.factory(definitely_infinite=True)
    def count(*args, **kwargs):
        return itertools.count(*args, **kwargs)
    
    my_count = count()
    assert isinstance(my_count, LazyTuple)
    assert repr(my_count) == '<LazyTuple: (...)>'
    assert my_count.definitely_infinite
    assert my_count[:10] == tuple(range(10))
    assert len(my_count) == 0
    

def test_finite_iterator():
    '''Test `LazyTuple` on a finite iterator.'''
    my_finite_iterator = iter(range(5))
    lazy_tuple = LazyTuple(my_finite_iterator)
    assert not lazy_tuple.is_exhausted

    assert list(itertools.islice(lazy_tuple, 0, 2)) == [0, 1]
    assert not lazy_tuple.is_exhausted
    assert repr(lazy_tuple) == '<LazyTuple: [0, 1]...>'
    
    second_to_last = lazy_tuple[-2]
    assert second_to_last == 3
    assert lazy_tuple.is_exhausted
    assert len(lazy_tuple) == lazy_tuple.known_length == \
           len(lazy_tuple.collected_data)
    assert repr(lazy_tuple) == '<LazyTuple: [0, 1, 2, 3, 4]>'
    assert LazyTuple(reversed(LazyTuple(reversed(lazy_tuple)))) == lazy_tuple
    
    assert 6 * lazy_tuple == 2 * lazy_tuple * 3 == lazy_tuple * 3 * 2 == \
           (0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4,
            0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4)
    
    assert lazy_tuple + ('meow', 'frr') == (0, 1, 2, 3, 4, 'meow', 'frr')
    assert ('meow', 'frr') + lazy_tuple == ('meow', 'frr', 0, 1, 2, 3, 4)

    
    identical_lazy_tuple = LazyTuple(iter(range(5)))
    assert not identical_lazy_tuple.is_exhausted
    my_dict = {}
    my_dict[identical_lazy_tuple] = 'flugzeug'
    assert identical_lazy_tuple.is_exhausted
    assert my_dict[lazy_tuple] == 'flugzeug'
    assert len(my_dict) == 1
    assert lazy_tuple == identical_lazy_tuple
    my_dict[lazy_tuple] = 'lederhosen'
    assert my_dict[identical_lazy_tuple] == 'lederhosen'
    assert len(my_dict) == 1
    

def test_immutable_sequence():
    '''Test that `LazyTuple` is considered an immutable sequence.'''
    assert sequence_tools.is_immutable_sequence(LazyTuple([1, 2, 3]))