# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''This module monkey-patches the pickling dispatch table using `copy_reg`.'''

# todo: alters global state, yuck! Maybe check before if it's already set to
# something?

import copy_reg
import types

from python_toolbox import import_tools


###############################################################################

def reduce_method(method):
    '''Reducer for methods.'''
    return (
        getattr,
        (
            
            method.im_self or method.im_class,
            # `im_self` for bound methods, `im_class` for unbound methods.
            
            method.im_func.__name__
        
        )
    )

copy_reg.pickle(types.MethodType, reduce_method)


###############################################################################


def reduce_module(module):
    '''Reducer for modules.'''
    return (import_tools.normal_import, (module.__name__,))

copy_reg.pickle(types.ModuleType, reduce_module)


###############################################################################


def _get_ellipsis():
    '''Get the `Ellipsis`.'''
    return Ellipsis

def reduce_ellipsis(ellipsis):
    '''Reducer for `Ellipsis`.'''
    return (
        _get_ellipsis,
        ()
    )

copy_reg.pickle(types.EllipsisType, reduce_ellipsis)


###############################################################################


