# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `BaseStepType` class.

See its documentation for more details.
'''
# todo: can do __instancehook__ shit later
# todo: inherit from uninstanciable.
# todo: should this be a metaclass?
# todo: this abc doesn't enforce anything since we don't instantiate.
# todo: cool idea: allow using this class as a decorator to step functions

import types

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import caching


class StepType(abc.ABCMeta):

    def __call__(cls, step_function):
        step_function._BaseStepType__step_type = cls
        return step_function

    
    def __instancecheck__(cls, thing):
         # blocktodo: test for when calling with BaseStep without prior cache
        if hasattr(thing, '_BaseStepType__step_type'):
            return issubclass(thing._BaseStepType__step_type, cls)
        else:
            match = cls.__raw_instance_check(thing)
            if match:    
                actual_function = (
                    thing.im_func if
                    isinstance(thing, types.MethodType)
                    else thing
                )
                actual_function._BaseStepType__step_type = cls
                
        return match
    

    def __raw_instance_check(cls, thing):
        #tododoc: justify lines
        if not callable(thing):
            return False
        
        match = cls.name_identifier in thing.__name__
        
        if match is False:
            return False
        
        all_name_identifiers = \
            [cls_.name_identifier for cls_ in BaseStep.__subclasses__()]
             
        superseding_name_identifiers = \
            [name_identifier for name_identifier in all_name_identifiers if
             (cls.name_identifier in name_identifier) and
             (cls.name_identifier is not name_identifier)]
        
        if any((superseding_name_identifier in thing.__name__) for
               superseding_name_identifier in superseding_name_identifiers):
            return False
        
        return True
    

    @staticmethod
    def get_step_type(thing):
        step_types = BaseStep.__subclasses__()
        matches = dict((step_type, step_type.__instancecheck__(thing)) for 
                       step_type in step_types)
        matching_step_types = [step_type for (step_type, match) in
                               matches.iteritems() if match is True]
        
        assert 0 <= len(matching_step_types) <= 1
        
        if matching_step_types:
            (matching_step_type,) = matching_step_types
            return matching_step_type
        else:
            return None
    
        
        
        #if 'step' not in name:
            #raise GarlicSimException(
                #"%s is not a step function-- It doesn't have the word 'step' in "
                #"it. If you want GarlicSim to use it as a step function, give it "
                #"a `.step_type` attribute pointing to a step type. (Like "
                #"`garlicsim.misc.simpack_grokker.step_types.SimpleStep`.)" \
                #% thing)
        
        #if 'inplace_step_generator' in name:
            #raise NotImplementedError('`inplace_step_generator` not yet '
                                      #'supported. It will probably become '
                                      #'available in GarlicSim 0.7 in mid-2011.')
            #return InplaceStepGenerator
        
        #elif 'inplace_step' in name:
            #raise NotImplementedError('`inplace_step` not yet '
                                      #'supported. It will probably become '
                                      #'available in GarlicSim 0.7 in mid-2011.')
            #return InplaceStep
        
        #elif 'history_step_generator' in name:
            #raise NotImplementedError('`history_step_generator` not yet. '
                                      #'supported. It will probably become '
                                      #'available in GarlicSim 0.7 in mid-2011.')
            #return HistoryStepGenerator
        
        #elif 'step_generator' in name:
            #return StepGenerator
        
        #elif 'history_step' in name:
            #return HistoryStep
        
        #else:
            #assert 'step' in name
            #return SimpleStep


            
class BaseStep(object):
    '''
    A type of step function.
    
    There are several different types of step functions with different
    advantages and disadvantages. See the
    `garlicsim.misc.simpack_grokker.step_types` package for a collection of
    various step types.
    '''
    __metaclass__ = StepType


    name_identifier = abc.abstractproperty()
    
    
    verbose_name = abc.abstractproperty()
    '''The verbose name of the step type.'''

    
    step_iterator_class = abc.abstractproperty()
    '''The step iterator class used for steps of this step type.'''    
    
    