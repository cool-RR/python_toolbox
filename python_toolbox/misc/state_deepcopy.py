# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StateCopy` class and `state_deepcopy` function.

See their documentation for more information.
'''

import copy

from garlicsim.general_misc.copy_mode import CopyMode
from garlicsim.general_misc.persistent import DontCopyPersistent


class StateCopy(DontCopyPersistent, CopyMode):
    '''
    A copy mode used in a step function to generate the next state.
    
    A popular design pattern in step functions is to `deepcopy` the old state,
    modify it, and then return it as the new state. When this is done, you
    should pass `StepCopy()` into the `deepcopy` function as a memo. This
    assures that certain objects get copied in the right way for this context.
    '''

    
def state_deepcopy(state):
    '''
    Deepcopy a state, producing an identical duplicate state.
    
    One of the differences between this and plain `deepcopy` is that this
    function makes sure not to copy `Persistent` objects.
    '''
    return copy.deepcopy(state,
                         StateCopy())