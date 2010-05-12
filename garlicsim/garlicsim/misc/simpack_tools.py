
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import caching

import garlicsim.misc.simpack_grokker

def get_from_state(state):
    '''tododoc: can take either state instance or class'''
    state_class = state if isinstance(state, type) else type(state)
    return _get_from_state_class(state_class)
    

@caching.cache
def _get_from_state_class(state_class):
    assert state_class.__name__ == 'State' # remove this limitation
    original_module_name = state_class.__module__
    short_address = misc_tools.shorten_class_address(original_module_name,
                                                     state_class.__name__)
    simpack_name = '.'.join(short_address.split('.')[:-1])
    simpack = __import__(simpack_name, fromlist=[''])
    try:
        garlicsim.misc.simpack_grokker.SimpackGrokker(simpack)
        # Will get cached.
    except garlicsim.misc.InvalidSimpack:
        raise garlicsim.misc.GarlicSimException('''Could not guess simpack \
correctly from state object.''')
    return simpack
    
    
def shorten_class_address(module_name, class_name):
    
    original_module = get_module(module_name)
    original_class = getattr(original_module, class_name)
    
    current_module_name = module_name
    
    last_successful_module_name = current_module_name
    
    while True:
        # Removing the last submodule from the module name:
        current_module_name = '.'.join(current_module_name.split('.')[:-1]) 
        
        if not current_module_name:
            # We've reached the top module and it's successful, can break now.
            break
        
        current_module = get_module(current_module_name)
        
        candidate_class = getattr(current_module, class_name, None)
        
        if candidate_class is original_class:
            last_successful_module_name = current_module_name
        else:
            break
        
    return '.'.join((last_successful_module_name, class_name))