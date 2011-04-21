# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `LazyList` class.

See its documentation for more information.
'''

import textwrap
from keyword import iskeyword
from operator import itemgetter
from functools import wraps
import itertools

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc import decorator_tools
from garlicsim.general_misc import sequence_tools


def _convert_int_index_to_exhaustion_point(index):
    assert isinstance(index, int)
    if index >= 0:
        return i
    else: # i < 0
        return infinity

    
class LazyTuple(object):
    ''' '''
    def __init__(self, iterable):
        was_given_a_sequence = sequence_tools.is_sequence(iterable)
        
        self.exhausted = True if was_given_a_sequence else False
        ''' '''
        
        self._collected_data = list(iterable) if was_given_a_sequence else []
        ''' '''
        
        self._iterator = None if was_given_a_sequence else iter(iterable)
        ''' '''
        
    @classmethod
    def factory(cls, callable):
        def inner(*args, **kwargs):
            return cls(callable(*args, **kwargs))
        return decorator_tools.decorator(inner, callable)
        
    
    @property
    def known_length(self):
        '''
        The number of items which have been taken from the internal iterator.
        '''
        return len(self._collected_data)
    
    
    def _exhaust(self, i):

        if self.exhausted:
            return
        
        if isinstance(i, int):
            exhaustion_point = _convert_int_index_to_exhaustion_point(i)
        elif isinstance(i, slice):
            exhaustion_point = max(
                _convert_int_index_to_exhaustion_point(i.start),
                _convert_int_index_to_exhaustion_point(i.stop)
            )
            
        while len(self._collected_data) <= exhaustion_point:
            try:
                self._collected_data.append(self._iterator.next())
            except StopIteration:
                self.exhausted = True
                break
           
            
    def __getitem__(self, i):
        self._exhaust(i)
        return self._collected_data[i]
            