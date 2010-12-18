# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `State` class.

See its documentation for more info.
'''

from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import address_tools
from garlicsim.general_misc.function_anchoring_type import \
     FunctionAnchoringType

import garlicsim


class State(object):
    '''
    A state describes a world state in the world of the simulation.
    
    It contains information about a "frozen moment" in the simulation.

    All the information about the state of the simulation should be saved in
    attributes of the state object.

    When a state is created, a `.clock` attribute should be assigned to it,
    specifying what time it is in this state.

    A state object must always be pickleable, as do all the attributes assigned
    to it.
    '''
    
    __metaclass__ = FunctionAnchoringType
    
    
    def __repr__(self):
        '''
        Get a string representation of the state.
        
        Example output:
        <garlicsim.data_structures.State with clock 32.3 at 0x1c822d0>
        ''' 
        return '<%s %sat %s>' % \
               (
                   address_tools.describe(type(self), shorten=True),
                   ('with clock %s ' % self.clock) if hasattr(self, 'clock')
                   else '',
                   hex(id(self))
               )

    create_root = None
    create_messy_root = None
    
    # Python 2.5 doesn't have `type.__eq__`, so we supply one:
    __eq__ = lambda self, other: (id(self) == id(other))
    
        
