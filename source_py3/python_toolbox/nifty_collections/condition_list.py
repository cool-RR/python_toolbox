# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import threading

import collections.abc


class ConditionList(collections.abc.MutableSequence):
    
    def __init__(self, iterable=None):
        self.__list = list(iterable) if iterable is not None else []
        self.__condition = threading.Condition()
        self.__new_items = []
        
    
    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise NotImplementedError("Setting a slice isn't implemented yet.")
        assert isinstance(index, int)
        with self.__condition:
            assert not self.__new_items
            old_value = self.__list[index]
            self.__list[index] = value
            if value != old_value:
                self.__new_items.append(value)
                self.__notify_all()
                

    def __delitem__(self, index):
        with self.__condition:
            del self.__list[index]

    def insert(self, index, value):
        assert isinstance(index, int)
        with self.__condition:
            assert not self.__new_items
            self.__list.insert(index, value)
            if value != old_value:
                self.__new_items.append(value)
                self.__notify_all()
    
    def __getitem__(self, index):
        with self.__condition:
            return self.__list[index]


    def __len__(self, ):
        with self.__condition:
            return len(self.__list)
        
        
    def notify_all(self):
        pass
    
    def wait_for(self, *items):
        
        
        