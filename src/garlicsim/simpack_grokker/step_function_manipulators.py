# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines functions for manipulating step functions.
"""

def non_history_step_generator_from_simple_step(step_function, old_state,
                                                *args, **kwargs):
    """
    Given a simple step function and an existing state, acts as a step
    generator.
    """
    current = old_state
    while True:
        current = step_function(current, *args, **kwargs)
        yield current
        
def history_step_generator_from_simple_step(step_function, history_browser,
                                            *args, **kwargs):
    """
    Given a simple history-step function and an history browser, acts as a step
    generator.
    """
    while True:
        yield step_function(history_browser, *args, **kwargs)
        
def simple_non_history_step_from_step_generator(generator, old_state,
                                                *args, **kwargs):
    """
    Given a step generator and a state, acts as a simple step function.
    """
    iterator = generator(old_state, *args, **kwargs)
    return iterator.next()

def simple_history_step_from_step_generator(generator, history_browser,
                                            *args, **kwargs):
    """
    Given a history step generator and a state, acts as a simple step function.
    """
    iterator = generator(history_browser, *args, **kwargs)
    return iterator.next()