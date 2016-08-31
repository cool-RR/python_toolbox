# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import threading

import collections.abc

from python_toolbox import context_management


class ConditionList(collections.abc.MutableSequence,
                    context_management.DelegatingContextManager):
    '''
    Thread synchronization tool.
    
    This is a complex tool for synchronizing threads, so let me explain how it
    works.
    
    `ConditionList` is similar to a Python `list`. You can add items to it,
    view the items in it, change their order, remove items, etc.
    
    What makes it different than a normal `list` is that it provides methods
    `wait_for` and `wait_for_missing` that let you orchestrate threads based on
    this list.
    
    `wait_for` receives a list of items (or just one) and makes the thread
    block until the `ConditionList` object contains all of these items, and
    then the thread results. `wait_for_missing` is the opposite, waiting for a
    specified list of items to *not* be in the `ConditionList`, and only then
    does the thread resume. (See the docstrings for these functions for more
    details about the arguments.)

    When is `ConditionList` useful? Maybe you have a thread that's
    
    blocktododoc
    '''
    
    def __init__(self, iterable=None):
        self.__list = list(iterable) if iterable is not None else []
        self.__condition = \
                         self.delegatee_context_manager = threading.Condition()
        
    
    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise NotImplementedError("Setting a slice isn't implemented yet.")
        assert isinstance(index, int)
        with self.__condition:
            self.__list[index] = value
            self.__notify_all()
                

    def __delitem__(self, index):
        with self.__condition:
            del self.__list[index]
            self.__notify_all()

    def insert(self, index, value):
        assert isinstance(index, int)
        with self.__condition:
            self.__list.insert(index, value)
            self.__notify_all()
    
    def __getitem__(self, index):
        with self.__condition:
            return self.__list[index]

    def __len__(self):
        with self.__condition:
            return len(self.__list)
        
        
    def __notify_all(self):
        with self.__condition:
            self.__condition.notify_all()
    
    def wait(self, *, timeout=None):
        from python_toolbox import sequence_tools
        with self.__condition:
            self.__condition.wait(timeout=timeout)
    
    def wait_for(self, *items, remove=False, timeout=None,
                 extra_predicate=lambda: True):
        from python_toolbox import sequence_tools
        with self.__condition:
            self.__condition.wait_for(
                lambda: (extra_predicate() and
                         sequence_tools.is_contained_in(items, self.__list))
            )
            if remove:
                sequence_tools.remove_items(items, self)
        
    def wait_for_missing(self, *missing_items, timeout=None,
                         extra_predicate=lambda: True):
        from python_toolbox import sequence_tools
        with self.__condition:
            self.__condition.wait_for(
                lambda: (extra_predicate() and
                         not sequence_tools.is_contained_in(missing_items,
                                                            self.__list))
            )
        
    def wait_for_empty(self, timeout=None, extra_predicate=lambda: True):
        from python_toolbox import sequence_tools
        with self.__condition:
            self.__condition.wait_for(
                lambda: (extra_predicate() and not self.__list)
            )
            
    def play_out(self, iterable):
        assert not self
        for item in iterable:
            self.append(item)
            self.wait_for_missing(item)
        
        
    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self.__list)
        
    