# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the list_simulate function. See its documentation for more
information.
'''

import copy
import warnings

from garlicsim.general_misc import cute_iter_tools

import garlicsim
import garlicsim.misc
import history_browser as history_browser_module # Avoiding name clash

__all__ = ["list_simulate"]

def list_simulate(simpack, state, iterations, *args, **kwargs):
    '''
    Simulate from the given state for the given number of iterations.

    A simpack must be passed as the first parameter. Any extraneous parameters
    will be passed to the step function.
    
    Returns a list that spans all the states, from the initial one given to
    the final one.
    '''
    simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    step_profile = garlicsim.misc.StepProfile(*args, **kwargs)
    
    if not hasattr(state, 'clock'):
        state = copy.deepcopy(state)        
        state.clock = 0
                      
    if simpack_grokker.history_dependent:
        return __history_list_simulate(simpack_grokker, state, iterations,
                                       step_profile)
    else: # It's a non-history-dependent simpack
        return __non_history_list_simulate(simpack_grokker, state, iterations,
                                           step_profile)

    
def __history_list_simulate(simpack_grokker, state, iterations,
                             step_profile=None):
    '''
    For history-dependent simulations only:
    
    Simulate from the given state for the given number of iterations.

    A simpack must be passed as the first parameter. Any extraneous parameters
    will be passed to the step function.
    
    Returns a list that spans all the states, from the initial one given to
    the final one.
    '''
    
    if step_profile is None: step_profile = garlicsim.misc.StepProfile()
    
    tree = garlicsim.data_structures.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    history_browser = history_browser_module.HistoryBrowser(path)
    
    iterator = simpack_grokker.step_generator(history_browser, step_profile)
    finite_iterator = cute_iter_tools.shorten(iterator, iterations)
    
    current_node = root
    for current_state in finite_iterator:
        current_node = tree.add_state(current_state, parent=current_node)
    
    return [node.state for node in path]


def __non_history_list_simulate(simpack_grokker, state, iterations,
                                step_profile=None):
    '''
    For non-history-dependent simulations only:
    
    Simulate from the given state for the given number of iterations.

    A simpack must be passed as the first parameter. Any extraneous parameters
    will be passed to the step function.
    
    Returns a list that spans all the states, from the initial one given to
    the final one.
    '''

    if step_profile is None: step_profile = garlicsim.misc.StepProfile()
    
    tree = garlicsim.data_structures.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    
    iterator = simpack_grokker.step_generator(state, step_profile)
    finite_iterator = cute_iter_tools.shorten(iterator, iterations)
    
    current_node = root
    for current_state in finite_iterator:
        current_node = tree.add_state(current_state, parent=current_node)
    
    return [node.state for node in path]
