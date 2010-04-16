# alters global state, yuck!

import copy_reg
import types

def reduce_method(method):
    return (getattr, (method.im_self, method.im_func.__name__))

copy_reg.pickle(types.MethodType, reduce_method)

def reduce_module(module):
    return (__import__, (module.__name__, {}, {}, [''])) # fromlist cruft

copy_reg.pickle(types.ModuleType, reduce_module)