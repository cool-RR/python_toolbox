# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import types

from garlicsim.general_misc.third_party import decorator

from garlicsim.misc import GarlicSimException

from .step_types import (SimpleStep, StepGenerator, HistoryStep,
                         HistoryStepGenerator, InplaceStep,
                         InplaceStepGenerator)


def get_step_type(step_function):
    # todo: have this raise a specific exception when getting something other
    # than a step function
    step_type_attribute = getattr(step_function, 'step_type', None)
    if step_type_attribute:
        return step_type_attribute
    else:
        step_type = _get_step_type(step_function)
        actual_function = (
            step_function.im_func if
            isinstance(step_function, types.MethodType)
            else step_function
        )
        actual_function.step_type = step_type
        return step_type


def _get_step_type(step_function):
    if not callable(step_function):
        raise GarlicSimException("%s is not a callable object, so it can't be "
                                 "a step function." % step_function)
    name = step_function.__name__
    
    if 'step' not in name:
        raise GarlicSimException(
            "%s is not a step function-- It doesn't have the word 'step' in "
            "it. If you want GarlicSim to use it as a step function, give it "
            "a `.step_type` attribute pointing to a step type. (Like "
            "`garlicsim.misc.simpack_grokker.step_types.SimpleStep`.)" \
            % step_function)
    
    if 'inplace_step_generator' in name:
        raise NotImplementedError('`inplace_step_generator` not yet '
                                  'supported. It will probably become '
                                  'available in GarlicSim 0.7 in mid-2011.')
        return InplaceStepGenerator
    
    elif 'inplace_step' in name:
        raise NotImplementedError('`inplace_step` not yet '
                                  'supported. It will probably become '
                                  'available in GarlicSim 0.7 in mid-2011.')
        return InplaceStep
    
    elif 'history_step_generator' in name:
        raise NotImplementedError('`history_step_generator` not yet. '
                                  'supported. It will probably become '
                                  'available in GarlicSim 0.7 in mid-2011.')
        return HistoryStepGenerator
    
    elif 'step_generator' in name:
        return StepGenerator
    
    elif 'history_step' in name:
        return HistoryStep
    
    else:
        assert 'step' in name
        return SimpleStep
    