# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox import comparison_tools

KEY, PREV, NEXT = range(3)


class BaseOrderedSet(collections.Set, collections.Sequence):
    '''
    Base class for `OrderedSet` and `FrozenOrderedSet`, i.e. set with an order.

    This behaves like a `set` except items have an order. (By default they're
    ordered by insertion order, but that order can be changed.)
    '''
    
    def __init__(self, iterable=None):
        self.clear()
        if iterable is not None:
            self |= iterable

    def __getitem__(self, index):
        for i, item in enumerate(self):
            if i == index:
                return item
        else:
            raise IndexError
        
    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map

    def add(self, key):
        '''
        Add an element to a set.
    
        This has no effect if the element is already present.
        '''
        if key not in self._map:
            end = self._end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self._map[key] = [key, curr, end]

    def discard(self, key):
        """
        Remove an element from a set if it is a member.
    
        If the element is not a member, do nothing.
        """
        if key in self._map:        
            key, prev, next = self._map.pop(key)
            prev[NEXT] = next
            next[PREV] = prev

    def __iter__(self):
        end = self._end
        curr = end[NEXT]
        while curr is not end:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self):
        end = self._end
        curr = end[PREV]
        while curr is not end:
            yield curr[KEY]
            curr = curr[PREV]

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        return (
            isinstance(other, collections.Set) and
            isinstance(other, collections.Sequence) and
            len(self) == len(other) and
            tuple(self) == tuple(other)
        )


class FrozenOrderedSet(BaseOrderedSet):
    '''
    A `frozenset` with an order.

    This behaves like a `frozenset` (i.e. a set that can't be changed after
    creation) except items have an order. (By default they're ordered by
    insertion order, but that order can be changed.)
    '''

class OrderedSet(BaseOrderedSet, collections.MutableSet):
    '''
    A `set` with an order.

    This behaves like a `set` except items have an order. (By default they're
    ordered by insertion order, but that order can be changed.)
    '''

    def move_to_end(self, key):
        '''
        Move an existing element to the end (or beginning if last==False).

        Raises KeyError if the element does not exist.
        When last=True, acts like a fast version of self[key]=self.pop(key).

        '''
        # Inefficient implementation until someone cares.
        if key in self:
            self.remove(key)
            self.add(key)
            
    
    def sort(self, key=None, reverse=False):
        '''
        Sort the items according to their keys, changing the order in-place.
        
        The optional `key` argument will be passed to the `sorted` function as
        a key function.
        '''
        # Inefficient implementation until someone cares.
        key_function = \
                   comparison_tools.process_key_function_or_attribute_name(key)
        sorted_members = sorted(tuple(self), key=key_function, reverse=reverse)
        
        self.clear()
        self |= sorted_members

    def clear(self):
        self._end = [] 
        self._end += [None, self._end, self._end]
        self._map = {}
        
        
    def add(self, key):
        '''
        Add an element to a set.
    
        This has no effect if the element is already present.
        '''
        if key not in self._map:
            end = self._end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self._map[key] = [key, curr, end]

    def discard(self, key):
        """
        Remove an element from a set if it is a member.
    
        If the element is not a member, do nothing.
        """
        if key in self._map:        
            key, prev, next = self._map.pop(key)
            prev[NEXT] = next
            next[PREV] = prev

    def pop(self, last=True):
        '''Remove and return an arbitrary set element.'''
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self) if last else iter(self))
        self.discard(key)
        return key


class EmittingOrderedSet(OrderedSet):
    '''An ordered set that emits to `.emitter` every time it's modified.'''
    
    def __init__(self, emitter, items=()):
        if emitter:
            from python_toolbox.emitting import Emitter
            assert isinstance(emitter, Emitter)
        self.emitter = emitter
        OrderedSet.__init__(self, items)

        
    def add(self, key):
        '''
        Add an element to a set.
    
        This has no effect if the element is already present.
        '''
        if key not in self._map:
            end = self._end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self._map[key] = [key, curr, end]
            if self.emitter:
                self.emitter.emit()

                
    def discard(self, key):
        '''
        Remove an element from a set if it is a member.
        
        If the element is not a member, do nothing.
        '''
        if key in self._map:        
            key, prev, next = self._map.pop(key)
            prev[NEXT] = next
            next[PREV] = prev
            if self.emitter:
                self.emitter.emit()

                
    def set_emitter(self, emitter):
        '''Set `emitter` to be emitted with on every modification.'''
        self.emitter = emitter