# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


# todo: can do __instancehook__ shit later
from .base_step_type import BaseStepType


class SimpleStep(StepType):
    pass


class StepGenerator(StepType):
    pass


class HistoryStep(StepType):
    pass


class HistoryStepGenerator(StepType):
    pass


class InplaceStep(StepType):
    pass


class InplaceStepGenerator(StepType):
    pass


step_types_list = [SimpleStep, StepGenerator, HistoryStep,
                   HistoryStepGenerator, InplaceStep, InplaceStepGenerator]