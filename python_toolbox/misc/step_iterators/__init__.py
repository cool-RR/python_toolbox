# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines a collection of step iterators, one for each step type.

See documentation of `garlicsim.misc.BaseStepIterator` for more details.
'''

from .step_iterator import StepIterator
from .step_generator_iterator import StepGeneratorIterator
from .history_step_iterator import HistoryStepIterator
from .duplicating_step_iterator import DuplicatingStepIterator
from .duplicating_step_generator_iterator import \
    DuplicatingStepGeneratorIterator
from .inplace_step_iterator import InplaceStepIterator
from .inplace_step_generator_iterator import InplaceStepGeneratorIterator