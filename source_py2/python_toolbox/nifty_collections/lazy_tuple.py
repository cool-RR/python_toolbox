# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import threading
import collections
import itertools
from python_toolbox.third_party import functools

from python_toolbox import misc_tools
from python_toolbox import decorator_tools
from python_toolbox import comparison_tools


infinity = float('inf')

class _SENTINEL(misc_tools.NonInstantiable):
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

    
@functools.total_ordering
class LazyTuple(collections.Sequence):
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
    
    If you're passing in an iterator you definitely know to be infinite,
    specify `definitely_infinite=True`.
    '''
    
    def __init__(self, iterable, definitely_infinite=False):
        was_given_a_sequence = isinstance(iterable, collections.Sequence) and \
                               not isinstance(iterable, LazyTuple)
        
        self.is_exhausted = True if was_given_a_sequence else False
        '''Flag saying whether the internal iterator is tobag exhausted.'''
        
        self.collected_data = iterable if was_given_a_sequence else []
        '''All the items that were collected from the iterable.'''
        
        self._iterator = None if was_given_a_sequence else iter(iterable)
        '''The internal iterator from which we get data.'''
        
        self.definitely_infinite = definitely_infinite
        '''
        The iterator is definitely infinite.
        
        The iterator might still be infinite if this is `False`, but if it's
        `True` then it's definitely infinite.
        '''
        
        self.lock = threading.Lock()
        '''Lock used while exhausting to make `LazyTuple` thread-safe.'''
        
        
    @classmethod
    @decorator_tools.helpful_decorator_builder
    def factory(cls, definitely_infinite=False):
        '''
        Decorator to make generators return a `LazyTuple`.
                
        Example:
        
            @LazyTuple.factory()
            def my_generator():
                yield 'hello'; yield 'world'; yield 'have'; yield 'fun'
        
        This works on any function that returns an iterator. todo: Make it work
        on iterator classes.
        '''
        
        def inner(function, *args, **kwargs):
            return cls(function(*args, **kwargs),
                       definitely_infinite=definitely_infinite)
        return decorator_tools.decorator(inner)
        
    
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
        from python_toolbox import sequence_tools
        
        if self.is_exhausted:
            return
        
        elif isinstance(i, int) or i == infinity:
            exhaustion_point = _convert_index_to_exhaustion_point(i)
            
        else:
            assert isinstance(i, slice)

            # todo: can be smart and figure out if it's an empty slice and then
            # not exhaust.
            
            canonical_slice = sequence_tools.CanonicalSlice(i)
            
            exhaustion_point = max(
                _convert_index_to_exhaustion_point(canonical_slice.start),
                _convert_index_to_exhaustion_point(canonical_slice.stop)
            )
            
            if canonical_slice.step > 0: # Compensating for excluded last item:
                exhaustion_point -= 1
            
        while len(self.collected_data) <= exhaustion_point:
            try:
                with self.lock:
                    self.collected_data.append(next(self._iterator))
            except StopIteration:
                self.is_exhausted = True
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
        if self.definitely_infinite:
            return 0 # Unfortunately infinity isn't supported.
        else:
            self.exhaust()
            return len(self.collected_data)

    
    def __eq__(self, other):
        from python_toolbox import sequence_tools
        if not sequence_tools.is_immutable_sequence(other):
            return False
        for i, j in itertools.izip_longest(self, other,
                                                 fillvalue=_SENTINEL):
            if (i is _SENTINEL) or (j is _SENTINEL):
                return False
            if i != j:
                return False
        return True
    
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    
    def __bool__(self):
        try: next(iter(self))
        except StopIteration: return False
        else: return True

    __nonzero__ = __bool__
    
    def __lt__(self, other):
        if not self and other:
            return True
        elif self and not other:
            return False
        elif not self and not other:
            return False
        for a, b in itertools.izip_longest(self, other,
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
        if self.is_exhausted:
            inner = repr(self.collected_data)
                             
        else: # not self.exhausted
            if self.collected_data == []:
                inner = '(...)'
            else: 
                inner = '%s...' % repr(self.collected_data)            
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
        if self.definitely_infinite:
            raise TypeError("An infinite `LazyTuple` isn't hashable.")
        else:
            self.exhaust()
            return hash(tuple(self))
        

collections.Sequence.register(LazyTuple)