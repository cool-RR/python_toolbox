# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.nifty_collections.LazyTuple`.'''

import uuid
import itertools

from garlicsim.general_misc.third_party import abcs_collection


from garlicsim.general_misc.nifty_collections import LazyTuple


class SelfAwareUuidIterator(abcs_collection.Iterator):
    def __init__(self):
        self.data = []
    def next(self):
        new_entry = uuid.uuid4()
        self.data.append(new_entry)
        return new_entry

    
def test():
    self_aware_uuid_iterator = SelfAwareUuidIterator()
    lazy_tuple = LazyTuple(self_aware_uuid_iterator)
    assert len(self_aware_random_iterator.data) == 0
    assert not lazy_tuple.exhausted
    
    first = lazy_tuple[0]
    assert len(self_aware_random_iterator.data) == 1
    assert isinstance(first, uuid.UUID)
    assert first == self_aware_random_iterator.data[0]
    
    first_ten = lazy_tuple[:10]
    assert isinstance(first_ten, tuple)
    assert len(self_aware_random_iterator.data) == 10
    assert first_ten[0] == first
    assert all(isinstance(item, uuid.UUID) for item in first_ten)
    
    weird_slice = lazy_tuple[15:5:-3]
    assert isinstance(first_ten, tuple)
    assert len(self_aware_random_iterator.data) == 16
    assert len(weird_slice) == 4
    assert weird_slice[2] == first_ten[-1] == lazy_tuple[9]
    assert not lazy_tuple.exhausted

    
def test_string():
    string = 'meow'
    lazy_tuple = LazyTuple(string)
    assert lazy_tuple.exhausted
    assert ''.join(lazy_tuple) == string
    assert ''.join(lazy_tuple[1:-1]) == string[1:-1]
    
    assert sorted((lazy_tuple, 'abc', 'xyz', 'meowa')) == \
           ['abc', lazy_tuple, 'meowa', 'xyz']
    
    
def test_infinite():
    lazy_tuple = LazyTuple(itertools.count())
    assert not lazy_tuple.exhausted
    lazy_tuple[100]
    assert len(lazy_tuple.collected_data) == 101
    assert not lazy_tuple.exhausted
    

def test_factory_decorator():
    @LazyTuple.factory
    def count(*args, **kwargs):
        return itertools.count(*args, **kwargs)
    
    my_count = count()
    assert isinstance(my_count, LazyTuple)
    assert my_count[:10] == tuple(xrange(10))
    
    
    