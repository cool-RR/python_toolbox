# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import threading

import collections.abc

from python_toolbox import context_management


class ConditionList(collections.abc.MutableSequence):
    
    def __init__(self, iterable=None):
        self.__list = list(iterable) if iterable is not None else []
        self.__condition = threading.Condition()
        
    
    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise NotImplementedError("Setting a slice isn't implemented yet.")
        assert isinstance(index, int)
        with self.__condition:
            old_value = self.__list[index]
            self.__list[index] = value
            if value != old_value:
                self.__notify_all()
                

    def __delitem__(self, index):
        with self.__condition:
            del self.__list[index]

    def insert(self, index, value):
        assert isinstance(index, int)
        with self.__condition:
            self.__list.insert(index, value)
            if value != old_value:
                self.__notify_all()
    
    def __getitem__(self, index):
        with self.__condition:
            return self.__list[index]


    def __len__(self, ):
        with self.__condition:
            return len(self.__list)
        
        
    def __notify_all(self):
        with self.__condition:
            self.__condition.notify_all()
    
    @context_management.ContextManagerType
    def wait_for(self, *items):
        from python_toolbox import sequence_tools
        with self.__condition:
            self.__condition.wait_for(
                    lambda: sequence_tools.is_contained_in(items, self.__list))
            yield
        
        