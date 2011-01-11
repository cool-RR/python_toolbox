# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `simulate` function.

See its documentation for more info.
'''

import copy
import warnings

from garlicsim.general_misc import cute_iter_tools

import garlicsim
import garlicsim.misc
from . import history_browser as history_browser_module # Avoiding name clash

__all__ = ['simulate']


def simulate(state, iterations=1, *args, **kwargs):
    '''
    Simulate from the given state for the given number of iterations.

    If you wish, in `*args` and `**kwargs` you may specify simulation
    parameters and/or a specific step function to use. (You may specify a step
    function either as the first positional argument or the `step_function`
    keyword argument.) You may also pass in an existing step profile.
    
    Returns the final state of the simulation.
    '''
    simpack_grokker = garlicsim.misc.SimpackGrokker.create_from_state(state)
    
    parse_arguments_to_step_profile = garlicsim.misc.StepProfile.build_parser(
        simpack_grokker.default_step_function
    )
    step_profile = parse_arguments_to_step_profile(*args, **kwargs)

    if not hasattr(state, 'clock'):
        # todo: make mechanism to prevent deepcopying twice, both here and
        # in inplace handling.
        state = garlicsim.misc.state_deepcopy.state_deepcopy(state)
        state.clock = 0
    
    if simpack_grokker.history_dependent:
        return __history_simulate(simpack_grokker, state, iterations,
                                  step_profile)
    else: # It's a non-history-dependent simpack
        return __non_history_simulate(simpack_grokker, state, iterations,
                                      step_profile)

    
def __history_simulate(simpack_grokker, state, iterations, step_profile):
    '''    
    Simulate from the given state for the given number of iterations.
    
    (Internal function, for history-dependent simulations only)
    
    Returns the final state of the simulation.
    '''
            
    tree = garlicsim.data_structures.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    history_browser = history_browser_module.HistoryBrowser(path)
    
    iterator = simpack_grokker.get_step_iterator(history_browser, step_profile)
    finite_iterator = cute_iter_tools.shorten(iterator, iterations)
    
    current_node = root
    current_state = current_node.state
    
    try:
        for current_state in finite_iterator:
            current_node = tree.add_state(current_state, parent=current_node)
    except garlicsim.misc.WorldEnded:
        pass
        
    final_state = current_state
    # Which is still here as the last value from the `for` loop.
    
    return final_state


def __non_history_simulate(simpack_grokker, state, iterations, step_profile):
    '''
    Simulate from the given state for the given number of iterations.
    
    (Internal function, for non-history-dependent simulations only.)
    
    Returns the final state of the simulation.
    '''
    
    # We try to get an inplace step iterator, if our simpack supplies one.
    # Otherwise we use a regular one. The reason we do it here in
    # `__non_history_simulate` is because this function gives the user only the
    # final state, without keeping any states in between. Therefore we can
    # afford doing the steps inplace, and we get better performance because we
    # don't deepcopy states.
    if simpack_grokker.is_inplace_iterator_available(step_profile) is True:
        state_copy = garlicsim.misc.state_deepcopy.state_deepcopy(state)
        iterator = \
            simpack_grokker.get_inplace_step_iterator(state_copy, step_profile)
        
    else: # Inplace iterator is not available
        iterator = simpack_grokker.get_step_iterator(state, step_profile)
    
    finite_iterator = cute_iter_tools.shorten(iterator, iterations)
    current_state = state
    
    try:
        for current_state in finite_iterator:
            pass
    except garlicsim.misc.WorldEnded:
        pass    
    
    final_state = current_state
    # Which is still here as the last value from the `for` loop.
    
    return final_state