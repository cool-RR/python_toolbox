# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module monkey-patches the pickling dispatch table using `copy_reg`.'''

# todo: alters global state, yuck! Maybe check before if it's already set to
# something?

import copy_reg
import types
import __builtin__

###############################################################################

def reduce_method(method):
    '''Reducer for methods.'''
    # todo: I have no idea how come it works for unbound methods. Because
    # unbound methods are still of the type `MethodType`, and their `.im_self`
    # is None, so how does it work? Possibly `pickle` actually knows how to
    # pickle unbound methods, and doesn't really use this?    
    return (getattr, (method.im_self, method.im_func.__name__))

copy_reg.pickle(types.MethodType, reduce_method)

###############################################################################

def __import__(*args, **kwargs):
    '''Wrapper for the builtin `__import__`'''
    # todo: This is needed when debugging in Wing, cause Wing replaces
    # `__import__` with its own. This feels bad.
    return __builtin__.__import__(*args, **kwargs)

def reduce_module(module):
    '''Reducer for modules.'''
    return (__import__, (module.__name__, {}, {}, [''])) # fromlist cruft

copy_reg.pickle(types.ModuleType, reduce_module)

###############################################################################