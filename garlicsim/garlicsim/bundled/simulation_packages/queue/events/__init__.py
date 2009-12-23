# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Package that defines an event system.

See documentation for EventSet.
'''

from event import Event
from event_set import EventSet


###############################################################################
import copy_reg
import types

def reduce_method(m):
    return (getattr, (m.im_self, m.im_func.__name__))

copy_reg.pickle(types.MethodType, reduce_method)

# alters global state, yuck!
###############################################################################