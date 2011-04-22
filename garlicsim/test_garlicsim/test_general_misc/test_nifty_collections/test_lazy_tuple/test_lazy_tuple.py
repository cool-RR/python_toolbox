# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.nifty_collections.LazyTuple`.'''

import uuid

from garlicsim.general_misc.third_party import abcs_collection


from garlicsim.general_misc.nifty_collections import LazyTuple


class SelfAwareRandomIterator(abcs_collection.Iterator):
    def __init__(self):
        self.data = []
    def next(self):
        new_entry = uuid.uuid4()
        self.data.append(new_entry)
        return new_entry

    
def test_lazy_tuple():
    self_aware_random_iterator = SelfAwareRandomIterator()
    lazy_tuple = LazyTuple(self_aware_random_iterator)
    assert len(self_aware_random_iterator.data) == 0
    
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
    
    
    
    
    
    
    
    
    
    
    
    