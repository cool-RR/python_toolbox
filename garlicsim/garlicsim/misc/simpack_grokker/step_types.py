# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


# todo: can do __instancehook__ shit later
from .base_step_type import BaseStepType
from garlicsim.misc import step_iterators


class SimpleStep(BaseStepType):
    step_iterator_class = step_iterators.StepIterator
    verbose_name = 'simple step function'


class StepGenerator(BaseStepType):
    verbose_name = 'step generator'
    pass
    
    
class HistoryStep(BaseStepType):
    step_iterator_class = step_iterators.HistoryStepIterator
    verbose_name = 'history step function'


class HistoryStepGenerator(BaseStepType):
    verbose_name = 'history step generator'
    pass


class InplaceStep(BaseStepType):
    inplace_step_iterator_class = 7
    verbose_name = 'inplace step function'
    pass


class InplaceStepGenerator(BaseStepType):
    inplace_step_iterator_class = 7
    verbose_name = 'inplace step generator'
    pass


step_types_list = [SimpleStep, StepGenerator, HistoryStep,
                   HistoryStepGenerator, InplaceStep, InplaceStepGenerator]