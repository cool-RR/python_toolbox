# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx
import abc

class CuteWindowType(type):
    def __new__(mcls, name, bases, namespace):
        cls = super(CuteWindowType, mcls).__new__(mcls, name, bases, namespace)
        callables = dict(
        for name, value in namespace.items():
            
        # Compute set of abstract method names
        abstracts = set(name
                     for name, value in namespace.items()
                     if getattr(value, "__isabstractmethod__", False))
        for base in bases:
            for name in getattr(base, "__abstractmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                    abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)
        # Set up inheritance registry
        cls._abc_registry = WeakSet()
        cls._abc_cache = WeakSet()
        cls._abc_negative_cache = WeakSet()
        cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        return cls

