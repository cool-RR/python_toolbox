# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `OrderedSet` class.

See its documentation for more details.
'''
# todo: revamp

import collections

from python_toolbox import comparison_tools


KEY, PREV, NEXT = range(3)


class OrderedSet(collections.MutableSet, collections.Sequence):
    '''
    A set with an order.
    
    You can also think of this as a list which doesn't allow duplicate items
    and whose `__contains__` method is O(1).
    '''

    def __init__(self, iterable=None):
        self.clear()
        if iterable is not None:
            self |= iterable


    def clear(self):
        self._end = [] 
        self._end += [None, self._end, self._end]
        self._map = {}
        
        
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
        """
        Add an element to a set.
    
        This has no effect if the element is already present.
        """
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

    def pop(self, last=True):
        """Remove and return an arbitrary set element."""
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self) if last else iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def __del__(self):
        self.clear()                    # remove circular references
        # todo: is this really needed? i'm worried about this making the gc not
        # drop circulary-referencing objects.

    def move_to_end(self, key):
        '''Move an existing element to the end (or beginning if last==False).

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
        
      