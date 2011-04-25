# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `LazyTuple` class.

See its documentation for more information.
'''

import itertools
import threading
import collections
from garlicsim.general_misc.third_party import abcs_collection

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc import decorator_tools
from garlicsim.general_misc import sequence_tools


class _SENTINEL(object):
    pass

def _convert_int_index_to_exhaustion_point(index):
    assert isinstance(index, int)
    if index >= 0:
        return index
    else: # i < 0
        return infinity


@decorator_tools.decorator
def with_lock(method, *args, **kwargs):
    '''
    Decorator for using the tree lock (in write mode) as a context manager.
    '''
    self = args[0]
    with self.lock:
        return method(*args, **kwargs)

    
#blocktodo: go over all sequence and tuple methods, see what I should add
class LazyTuple(abcs_collection.Sequence, object):
    ''' '''
    def __init__(self, iterable):
        was_given_a_sequence = sequence_tools.is_sequence(iterable)
        
        self.exhausted = True if was_given_a_sequence else False
        ''' '''
        
        self.collected_data = list(iterable) if was_given_a_sequence else []
        ''' '''
        
        self._iterator = None if was_given_a_sequence else iter(iterable)
        ''' '''
        
        self.lock = threading.Lock()
        
        
    @classmethod
    def factory(cls, callable):
        def inner(function, *args, **kwargs):
            return cls(callable(*args, **kwargs))
        return decorator_tools.decorator(inner, callable)
        
    
    @property
    def known_length(self):
        '''
        The number of items which have been taken from the internal iterator.
        '''
        return len(self.collected_data)
    

    @with_lock
    def _exhaust(self, i=None):

        if self.exhausted:
            return
        
        if i is None:
            exhaustion_point = infinity
        
        elif isinstance(i, int):
            exhaustion_point = _convert_int_index_to_exhaustion_point(i)
            
        else
            assert isinstance(i, slice):

            # todo: can be smart and figure out if it's an empty slice and then
            # not exhaust.
            
            (start, stop, step) = sequence_tools.parse_slice(i)
            
            exhaustion_point = max(
                _convert_int_index_to_exhaustion_point(start),
                _convert_int_index_to_exhaustion_point(stop)
            )
            
            if step > 0: # Compensating for excluded last item:
                exhaustion_point -= 1
            
        while len(self.collected_data) <= exhaustion_point:
            try:
                self.collected_data.append(self._iterator.next())
            except StopIteration:
                self.exhausted = True
                break
           
            
    def __getitem__(self, i):
        self._exhaust(i)
        result = self.collected_data[i]
        if isinstance(i, slice):
            return tuple(result)
        else:
            return result
            
    
    def __len__(self):
        self._exhaust()
        return len(self.collected_data)

    
    def __eq__(self, other):
        if not sequence_tools.is_immutable_sequence(other):
            return False
        for i, j in cute_iter_tools.izip_longest(self, other,
                                                 fillvalue=_SENTINEL):
            if (i is _SENTINEL) or (j is _SENTINEL):
                return False
            if i != j:
                return False
        return True
    
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    
    def __nonzero__(self):
        self._exhaust(0)
        return bool(self.collected_data)

    
    def __lt__(self, other):
        '''
        This method returns ``True`` if this list is "lower than" the given
        `other` list. This is the case if...

        - this list is empty and the other is not.
        - the first nth item in this list which is unequal to the
          corresponding item in the other list, is lower than the corresponding
          item.

        If this and the other list is empty this method will return ``False``.
        '''
        if not self and other:
            return True
        elif self and not other:
            return False
        elif not self and not other:
            return False
        for a, b in cute_iter_tools.izip_longest(self, other,
                                                 fillvalue=_SENTINEL):
            if a < b:
                return True
            elif a == b:
                continue
            elif a is _SENTINEL and b is not _SENTINEL:
                return True
            return False

        
    def __gt__(self, other):
        '''
        This method returns ``True`` if this list is "greater than" the given
        `other` list. This is the case if...

        - this list is not empty and the other is
        - the first nth item in this list which is unequal to the
          corresponding item in the other list, is greater than the
          corresponding item.

        If this and the other list is empty this method will return ``False``.
        '''

        if not self and not other:
            return False
        return not self.__lt__(other)
    
    
    def __repr__(self):
        '''
        Returns the representation string of the list, if the list exhausted
        this looks like the representation of any other list, otherwise the
        "lazy" part is represented by '...', like '[1, 2, 3, ...]'.
        '''
        if self.exhausted:
            inner = ''.join(('(',                             
                             repr(self.collected_data)[1:-1],
                             ')'))
                             
        else: # not self.exhausted
            if self.collected_data == ():
                inner = '()'
            else: 
                inner = ''.join(('(',
                                 repr(self.collected_data)[1:-1],
                                 ' ...)'))
            
        return '<%s: %s>' % (self.__class__.__name__, inner) 
    
    
if hasattr(collections, 'Sequence'):
    collections.Sequence.register(LazyTuple)