# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `LazyTuple` class.

See its documentation for more information.
'''

import threading
import collections

from python_toolbox import cute_iter_tools
from python_toolbox import decorator_tools
from python_toolbox import comparison_tools
from python_toolbox import sequence_tools


infinity = float('inf')

class _SENTINEL:
    '''Sentinel used to detect the end of an iterable.'''
    

def _convert_index_to_exhaustion_point(index):
    '''
    Convert an index to an "exhaustion point".
    
    The index may be either an integer or infinity.
    
    "Exhaustion point" means "until which index do we need to exhaust the
    internal iterator." If an index of `3` was requested, we need to exhaust it
    to index `3`, but if `-7` was requested, we have no choice but to exhaust
    the iterator completely (i.e. to `infinity`, actually the last element,)
    because only then we could know which member is the seventh-to-last.    
    '''
    assert isinstance(index, int) or index == infinity
    if index >= 0:
        return index
    else: # i < 0
        return infinity


@decorator_tools.decorator
def _with_lock(method, *args, **kwargs):
    '''Decorator for using the `LazyTuple`'s lock.'''
    self = args[0]
    with self.lock:
        return method(*args, **kwargs)

    
class LazyTuple(collections.Sequence, object):
    '''
    A lazy tuple which requests as few values as possible from its iterator.
    
    Wrap your iterators with `LazyTuple` and enjoy tuple-ish features like
    indexed access, comparisons, length measuring, element counting and more.
    
    Example:
    
        def my_generator():
            yield 'hello'; yield 'world'; yield 'have'; yield 'fun'
            
        lazy_tuple = LazyTuple(my_generator())
        
        assert lazy_tuple[2] == 'have'
        assert len(lazy_tuple) == 4
    
    `LazyTuple` holds the given iterable and pulls items out of it. It pulls as
    few items as it possibly can. For example, if you ask for the third
    element, it will pull exactly three elements and then return the third one.
    
    Some actions require exhausting the entire iterator. For example, checking
    the `LazyTuple` length, or doing indexex access with a negative index.
    (e.g. asking for the seventh-to-last element.)
    '''
    
    def __init__(self, iterable):
        was_given_a_sequence = sequence_tools.is_sequence(iterable) and \
                               not isinstance(iterable, LazyTuple)
        
        self.exhausted = True if was_given_a_sequence else False
        '''Flag saying whether the internal iterator is totally exhausted.'''
        
        self.collected_data = list(iterable) if was_given_a_sequence else []
        '''All the items that were collected from the iterable.'''
        
        self._iterator = None if was_given_a_sequence else iter(iterable)
        '''The internal iterator from which we get data.'''
        
        self.lock = threading.Lock()
        '''Lock used while exhausting to make `LazyTuple` thread-safe.'''
        
        
    @classmethod
    def factory(cls, callable):
        '''
        Decorator to make generators return a `LazyTuple`.
                
        Example:
        
            @LazyTuple.factory
            def my_generator():
                yield 'hello'; yield 'world'; yield 'have'; yield 'fun'
        
        This works on any function that returns an iterator. todo: Make it work
        on iterator classes.
        '''
        
        def inner(function, *args, **kwargs):
            return cls(callable(*args, **kwargs))
        return decorator_tools.decorator(inner, callable)
        
    
    @property
    def known_length(self):
        '''
        The number of items which have been taken from the internal iterator.
        '''
        return len(self.collected_data)
    

    def exhaust(self, i=infinity):
        '''
        Take items from the internal iterators and save them.
        
        This will take enough items so we will have `i` items in total,
        including the items we had before.
        '''
        if self.exhausted:
            return
        
        elif isinstance(i, int) or i == infinity:
            exhaustion_point = _convert_index_to_exhaustion_point(i)
            
        else:
            assert isinstance(i, slice)

            # todo: can be smart and figure out if it's an empty slice and then
            # not exhaust.
            
            (start, stop, step) = sequence_tools.parse_slice(i)
            
            exhaustion_point = max(
                _convert_index_to_exhaustion_point(start),
                _convert_index_to_exhaustion_point(stop)
            )
            
            if step > 0: # Compensating for excluded last item:
                exhaustion_point -= 1
            
        while len(self.collected_data) <= exhaustion_point:
            try:
                with self.lock:
                    self.collected_data.append(next(self._iterator))
            except StopIteration:
                self.exhausted = True
                break
           
            
    def __getitem__(self, i):
        '''Get item by index, either an integer index or a slice.'''
        self.exhaust(i)
        result = self.collected_data[i]
        if isinstance(i, slice):
            return tuple(result)
        else:
            return result
            
    
    def __len__(self):
        self.exhaust()
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
    
    
    def __bool__(self):
        self.exhaust(0)
        return bool(self.collected_data)

    
    def __lt__(self, other):
        if not self and other:
            return True
        elif self and not other:
            return False
        elif not self and not other:
            return False
        for a, b in cute_iter_tools.izip_longest(self, other,
                                                 fillvalue=_SENTINEL):
            if a is _SENTINEL:
                # `self` ran out. Now there can be two cases: (a) `other` ran
                # out too or (b) `other` didn't run out yet. In case of (a), we
                # have `self == other`, and in case of (b), we have `self <
                # other`. In any case, `self <= other is True` so we can
                # unconditionally return `True`.
                return True            
            elif b is _SENTINEL:
                assert a is not _SENTINEL
                return False
            elif a == b:
                continue
            elif a < b:
                return True
            else:
                assert a > b
                return False
    
    
    def __repr__(self):
        '''
        Return a human-readeable representation of the `LazyTuple`.
        
        Example:
        
            <LazyTuple: (1, 2, 3, ...)>
            
        The '...' denotes a non-exhausted lazy tuple.
        '''
        if self.exhausted:
            inner = ''.join(('(',                             
                             repr(self.collected_data)[1:-1],
                             ')'))
                             
        else: # not self.exhausted
            if self.collected_data == []:
                inner = '(...)'
            else: 
                inner = ''.join(('(',
                                 repr(self.collected_data)[1:-1],
                                 ', ...)'))
            
        return '<%s: %s>' % (self.__class__.__name__, inner) 
    
    
    def __add__(self, other):
        return tuple(self) + tuple(other)
    
    
    def __radd__(self, other):
        return tuple(other) + tuple(self)
    
    
    def __mul__(self, other):
        return tuple(self).__mul__(other)
    
    
    def __rmul__(self, other):
        return tuple(self).__rmul__(other)
    
    
    def __hash__(self):
        '''
        Get the `LazyTuple`'s hash.
        
        Note: Hashing the `LazyTuple` will completely exhaust it.
        '''
        self.exhaust()
        return hash(tuple(self))
    
    
comparison_tools.total_ordering(LazyTuple)

if hasattr(collections, 'Sequence'):
    collections.Sequence.register(LazyTuple)
    