# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StepType` class and its base instance, `BaseStep`.

See its documentation for more details.
'''
# todo: does this mixed abc enforce anything, with our custom `__call__`?
# todo: allow function with 'step' to opt-out of being a step function

import types

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import logic_tools
from garlicsim.general_misc import caching


class StepType(abc.ABCMeta):
    '''
    A type of step function.
    
    There are several different types of step functions with different
    advantages and disadvantages. See the
    `garlicsim.misc.simpack_grokker.step_types` package for a collection of
    various step types.
    
    You don't need to interact with step types (i.e. instances of this
    metaclass) in order to make step functions; If they have the appropriate
    name identifier in their name, they will be associated with a step type
    automaticaly. For example, a function called `meow_step_generator` will
    automatically be identified as a `StepGenerator`. (Which is one example of
    an instance of this metaclass.) So `isinstance(meow_step_generator,
    StepGenerator)` will be `True` and
    `StepType.get_step_type(meow_step_generator)` will be `StepGenerator`.
    
    One place where you do need to use this class is if your step function has
    a custom name. For example, you have a function `yambambula` and you want
    it to be identified as a `StepGenerator`. So you define it like this:
    
        @garlicsim.misc.simpack_grokker.step_types.StepGenerator
        def yambambula(self):
           ...
    
    Then the `yambambula` function will be identified as a step generator.
    '''

    def __call__(cls, step_function):
        '''
        Create a step function.
        
        Only necessary for step functions that don't have a valid name
        identifier (like "step") in their name.
        
        Usually used as a decorator.
        '''
        
        step_function._BaseStepType__step_type = cls
        return step_function

    
    def __instancecheck__(cls, thing):
        '''
        Check whether `thing` is a step function of this type.
        
        Given the base class `BaseType` as `cls`, it will check whether `thing`
        is a step function in general.
        '''
        
        step_type = StepType.get_step_type(thing)
        if step_type:
            return issubclass(step_type, cls)
        else:
            assert step_type is None
            return False
        
    
    @staticmethod
    def get_step_type(thing):
        '''Get what type of step function `thing` is.'''
        
        if hasattr(thing, '_BaseStepType__step_type'):
            return thing._BaseStepType__step_type
        
        if not callable(thing) or not hasattr(thing, '__name__'):
            return None
        
        step_types = BaseStep.__subclasses__()
        
        all_name_identifiers = [cls_.name_identifier for cls_ in step_types]        
                
        matching_name_identifiers = \
            [name_identifier for name_identifier in all_name_identifiers if
             name_identifier in thing.__name__]
        
        if not matching_name_identifiers:
            step_type = None
                    
        else:
            (maximal_matching_name_identifier,) = logic_tools.logic_max(
                matching_name_identifiers,
                relation=str.__contains__
            )
            
            (step_type,) = \
                [step_type for step_type in step_types if
                 step_type.name_identifier == maximal_matching_name_identifier]
        
        actual_function = (
            thing.im_func if
            isinstance(thing, types.MethodType)
            else thing
        )
        actual_function._BaseStepType__step_type = step_type
            
        return step_type
        
                
class BaseStep(object):
    '''Abstract step function. See documentation of `StepType`.'''
    
    __metaclass__ = StepType


    name_identifier = abc.abstractproperty()
    '''
    String that automatically identifies a step function's type.
    
    For example, `StepGenerator` has a `.name_identifier` of
    `'step_generator'`, so any function containing it (like
    `my_cool_step_generator`) will be automatically identified as a step
    generator.
    '''
    
    
    verbose_name = abc.abstractproperty()
    '''The verbose name of the step type.'''

    
    step_iterator_class = abc.abstractproperty()
    '''The step iterator class used for steps of this step type.'''    
    
    