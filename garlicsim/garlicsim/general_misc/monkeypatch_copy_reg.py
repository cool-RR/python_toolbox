# alters global state, yuck!

import copy_reg
import types
import __builtin__

###############################################################################

def reduce_method(method):
    return (getattr, (method.im_self, method.im_func.__name__))

copy_reg.pickle(types.MethodType, reduce_method)

###############################################################################

def __import__(*args, **kwargs):
    # todo: This is needed when debugging in Wing, cause Wing replaces
    # `__import__` with its own. This feels bad.
    return __builtin__.__import__(*args, **kwargs)

def reduce_module(module):
    return (__import__, (module.__name__, {}, {}, [''])) # fromlist cruft

copy_reg.pickle(types.ModuleType, reduce_module)

###############################################################################