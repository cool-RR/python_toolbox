# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines tools related to copying and deepcopying operations.
'''

import copy


def deepcopy_as_simple_object(thing, memo=None):
    '''
    Deepcopy an object as a simple `object`, ignoring any __deepcopy__ method.
    '''
    if memo is None:
        memo = {}
    klass = thing.__class__
    new_thing = klass.__new__(klass)
    memo[id(thing)] = new_thing
    for (name, subthing) in vars(thing).items():
        new_thing.__dict__[name] = copy.deepcopy(subthing, memo)
    return new_thing
        
    