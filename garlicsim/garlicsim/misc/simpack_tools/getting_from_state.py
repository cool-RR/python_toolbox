# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `get_from_state` function.

See its documentation for more information.
'''

from garlicsim.general_misc import address_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import caching


import garlicsim.misc.simpack_grokker


def get_from_state(state):
    '''Find the simpack that a state class (or a state instance) belong to.'''
    state_class = state if isinstance(state, type) else type(state)
    return get_from_state_class(state_class)
    

@caching.cache()
def get_from_state_class(state_class):
    '''
    Find the simpack that a state class belongs to.
    
    Internal use.
    '''
    assert state_class.__name__ == 'State' # remove this limitation
    short_address = address_tools.describe(state_class, shorten=True)
    simpack_name = '.'.join(short_address.split('.')[:-1])
    simpack = import_tools.normal_import(simpack_name)
        
    garlicsim.misc.simpack_grokker.SimpackGrokker(simpack)
    # Not saving the reference: But it'll get cached because `SimpackGrokker`
    # is a `CachedType`.
        
    return simpack


