# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


# todo: can do __instancehook__ shit later
from .base_step_type import BaseStepType
from garlicsim.misc import step_iterators


class SimpleStep(BaseStepType):
    step_iterator_class = step_iterators.StepIterator


class StepGenerator(BaseStepType):
    pass
    
    
class HistoryStep(BaseStepType):
    step_iterator_class = step_iterators.HistoryStepIterator


class HistoryStepGenerator(BaseStepType):
    pass


class InplaceStep(BaseStepType):
    inplace_step_iterator_class = 7
    pass


class InplaceStepGenerator(BaseStepType):
    inplace_step_iterator_class = 7
    pass


step_types_list = [SimpleStep, StepGenerator, HistoryStep,
                   HistoryStepGenerator, InplaceStep, InplaceStepGenerator]