# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for working with simpacks.'''


from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import caching

import garlicsim.misc.simpack_grokker


def get_from_state(state):
    '''Find the simpack that a state class (or a state instance) belong to.'''
    state_class = state if isinstance(state, type) else type(state)
    return _get_from_state_class(state_class)
    

@caching.cache
def _get_from_state_class(state_class):
    '''
    Find the simpack that a state class belong to.
    
    Internal use.
    '''
    assert state_class.__name__ == 'State' # remove this limitation
    original_module_name = state_class.__module__
    short_address = misc_tools.shorten_class_address(original_module_name,
                                                     state_class.__name__)
    simpack_name = '.'.join(short_address.split('.')[:-1])
    simpack = __import__(simpack_name, fromlist=[''])
    try:
        garlicsim.misc.simpack_grokker.SimpackGrokker(simpack)
        # Not saving the reference: But it'll get cached because SimpackGrokker
        # is a CachedType.
    except garlicsim.misc.InvalidSimpack:
        raise garlicsim.misc.GarlicSimException('''Could not guess simpack \
correctly from state object.''')
    return simpack
    
    