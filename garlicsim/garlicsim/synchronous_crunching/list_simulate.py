# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `list_simulate` function.

See its documentation for more info.
'''

import copy

from garlicsim.general_misc import cute_iter_tools

import garlicsim
import garlicsim.misc
from . import history_browser as history_browser_module # Avoiding name clash


__all__ = ['list_simulate']


def list_simulate(state, iterations, *args, **kwargs):
    '''
    Simulate from the given state for the given number of iterations.
    
    Returns a list that spans all the states, from the initial one given to
    the final one.
    
    If you wish, in `*args` and `**kwargs` you may specify simulation
    parameters and/or a specific step function to use. (You may specify a step
    function either as the first positional argument or the `step_function`
    keyword argument.) You may also pass in an existing step profile.
    '''
    simpack_grokker = garlicsim.misc.SimpackGrokker.create_from_state(state)
    
    parse_arguments_to_step_profile = garlicsim.misc.StepProfile.build_parser(
        simpack_grokker.default_step_function
    )
    step_profile = parse_arguments_to_step_profile(*args, **kwargs)
    
    if not hasattr(state, 'clock'):
        state = garlicsim.misc.state_deepcopy.state_deepcopy(state)
        state.clock = 0
                      
    if simpack_grokker.history_dependent:
        return _history_list_simulate(simpack_grokker, state, iterations,
                                      step_profile)
    else: # It's a non-history-dependent simpack
        return _non_history_list_simulate(simpack_grokker, state, iterations,
                                          step_profile)

    
def _history_list_simulate(simpack_grokker, state, iterations,
                           step_profile):
    '''
    Simulate from the given state for the given number of iterations.

    (Internal function for history-dependent simulations only.)    
    
    Returns a list that spans all the states, from the initial one given to
    the final one.
    '''
    
    tree = garlicsim.data_structures.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    history_browser = history_browser_module.HistoryBrowser(path)
    
    iterator = simpack_grokker.get_step_iterator(history_browser, step_profile)
    finite_iterator = cute_iter_tools.shorten(iterator, iterations)
    
    current_node = root
    current_state = current_node.state
    
    world_ended = False
    try:
        for current_state in finite_iterator:
            current_node = tree.add_state(current_state, parent=current_node)
    except garlicsim.misc.WorldEnded:
        world_ended = True
    
    # Not doing anything with `world_ended` yet
        
    return [node.state for node in path]


def _non_history_list_simulate(simpack_grokker, state, iterations,
                               step_profile):
    '''
    Simulate from the given state for the given number of iterations.
    
    (Internal function for non-history-dependent simulations only.)
    
    Returns a list that spans all the states, from the initial one given to
    the final one.
    '''

    tree = garlicsim.data_structures.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    
    iterator = simpack_grokker.get_step_iterator(state, step_profile)
    finite_iterator = cute_iter_tools.shorten(iterator, iterations)
    
    current_node = root
    current_state = current_node.state
    
    world_ended = False
    try:
        for current_state in finite_iterator:
            current_node = tree.add_state(current_state, parent=current_node)
    except garlicsim.misc.WorldEnded:
        world_ended = True

    # Not doing anything with `world_ended` yet
    
    return [node.state for node in path]

