# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''This module monkey-patches the pickling dispatch table using `copyreg`.'''

# todo: alters global state, yuck! Maybe check before if it's already set to
# something?

import copyreg
import types

from python_toolbox import import_tools


###############################################################################

def reduce_method(method):
    '''Reducer for methods.'''
    return (
        getattr,
        (

            method.__self__ or method.__self__.__class__,
            # `im_self` for bound methods, `im_class` for unbound methods.

            method.__func__.__name__

        )
    )

copyreg.pickle(types.MethodType, reduce_method)


###############################################################################


def reduce_module(module):
    '''Reducer for modules.'''
    return (import_tools.normal_import, (module.__name__,))

copyreg.pickle(types.ModuleType, reduce_module)


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

copyreg.pickle(type(Ellipsis), reduce_ellipsis)


###############################################################################


