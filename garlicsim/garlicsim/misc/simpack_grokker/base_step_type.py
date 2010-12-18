# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `BaseStepType` class.

See its dcoumentation for more details.
'''
# todo: can do __instancehook__ shit later
# todo: inherit from uninstanciable.
# todo: should this be a metaclass?
# todo: this abc doesn't enforce anything since we don't instantiate.

from garlicsim.general_misc.third_party import abc


class BaseStepType(object):
    '''
    A type of step function.
    
    There are several different types of step functions with different
    advantages and disadvantages. See the
    `garlicsim.misc.simpack_grokker.step_types` package for a collection of
    various step types.
    '''
    __metaclass__ = abc.ABCMeta
    
    verbose_name = abc.abstractproperty()
    '''The verbose name of the step type.'''
    
    step_iterator_class = abc.abstractproperty()
    '''The step iterator class used for steps of this step type.'''