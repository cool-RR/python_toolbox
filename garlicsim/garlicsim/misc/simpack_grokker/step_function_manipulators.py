# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines functions for manipulating step functions.

This module is technical.
'''

from garlicsim.misc import AutoClockGenerator

def non_history_step_generator_from_simple_step(step_function, old_state,
                                                *args, **kwargs):
    '''
    Given a simple step function and an existing state, acts as a step
    generator.
    '''
    
    current = old_state
    
    auto_clock_generator = AutoClockGenerator()
    auto_clock_generator.make_clock(current)
                                    
    while True:
        current = step_function(current, *args, **kwargs)
        current.clock = auto_clock_generator.make_clock(current)
        yield current        

def non_history_simple_step_from_step_generator(generator, old_state,
                                                *args, **kwargs):
    '''
    Given a step generator and a state, acts as a simple step function.
    '''
    iterator = generator(old_state, *args, **kwargs)
    return iterator.next()

#def non_history_simple_step_wrapper

def history_step_generator_from_simple_step(step_function, history_browser,
                                            *args, **kwargs):
    '''
    Given a simple history-step function and an history browser, acts as a step
    generator.
    '''
    while True:
        yield step_function(history_browser, *args, **kwargs)

def history_simple_step_from_step_generator(generator, history_browser,
                                            *args, **kwargs):
    '''
    Given a history step generator and a state, acts as a simple step function.
    '''
    iterator = generator(history_browser, *args, **kwargs)
    return iterator.next()