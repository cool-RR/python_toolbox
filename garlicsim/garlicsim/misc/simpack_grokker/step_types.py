# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A collection of step types.

See documentation for
`garlicsim.misc.simpack_grokker.step_type.StepType` for more details.
'''

from .step_type import BaseStep
from garlicsim.misc import step_iterators


class SimpleStep(BaseStep):
    '''The simplest step function. Takes a state and returns a new one.'''
    step_iterator_class = step_iterators.StepIterator
    name_identifier = 'step'
    verbose_name = 'simple step function'


class StepGenerator(BaseStep):
    '''
    A step generator takes an initial state and keeps yielding states from it.
    
    Some steps are easier to write as a step generator, because every time they
    yield a state they remember in which line they paused and what the values
    of all the local variables are.
    '''
    step_iterator_class = step_iterators.StepGeneratorIterator
    name_identifier = 'step_generator'
    verbose_name = 'step generator'
    
    
class HistoryStep(BaseStep):
    '''
    A history step function takes a history browser and returns a new state.
    
    The advantage of the history function is that it allows looking not only at
    the last state but at all the states in the timeline. This is necessary for
    some types of simulations.
    '''
    step_iterator_class = step_iterators.HistoryStepIterator
    name_identifier = 'history_step'
    verbose_name = 'history step function'


class HistoryStepGenerator(BaseStep):
    '''
    A history step generator takes a history browser and yields new states.
    
    This combines the advantages of a history step function and a step
    generator; it works as a generator which can be more convenient and it can
    look at the simulation history which is necessary for some simulations.
    
    (08.08.2011 - Not yet implemented, sorry.)
    '''
    step_iterator_class = NotImplemented
    name_identifier = 'history_step_generator'
    verbose_name = 'history step generator'
    
    
class InplaceStep(BaseStep):
    '''
    Inplace step function takes a state and modifies it to be the next state.
    
    The advantage of the inplace step function is that it doesn't need to
    create a new state object, so it may have better performance than a simple
    step function. But if the user still wants it to create new state objects,
    (which is necessary in order to make a tree,) `garlicsim` will
    automatically `deepcopy` all the states given from the inplace step
    function. So it can be used both ways.
    '''
    step_iterator_class = step_iterators.DuplicatingStepIterator
    inplace_step_iterator_class = step_iterators.InplaceStepIterator
    name_identifier = 'inplace_step'
    verbose_name = 'inplace step function'
    
    
class InplaceStepGenerator(BaseStep):
    '''
    Inplace step generator is a step generator that does the step in-place.
    
    On every iteration, the inplace step generator modifies the current state
    to be the next state.
    
    The inplace step generator combines the advantages an inplace step function
    and a step generator: It works as a generator which can be more convenient
    and it allows modifying the state in-place to improve performance.
    '''
    step_iterator_class = step_iterators.DuplicatingStepGeneratorIterator
    inplace_step_iterator_class = step_iterators.InplaceStepGeneratorIterator
    name_identifier = 'inplace_step_generator'
    verbose_name = 'inplace step generator'


step_types_list = [SimpleStep, StepGenerator, HistoryStep,
                   HistoryStepGenerator, InplaceStep, InplaceStepGenerator]
'''List of all the step types.'''
