# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import sys

import nose.tools

from garlicsim.misc.simpack_grokker.step_type import BaseStep, StepType
from garlicsim.misc.simpack_grokker import step_types as step_types_module

step_types = [thing for thing in vars(step_types_module).values() if 
              getattr(thing, '__module__', '').endswith('step_types')]

def test():
    assert type(BaseStep) is StepType
    for step_type in step_types:
        assert issubclass(step_type, BaseStep)
        assert type(step_type) is StepType
     
        
def test_uncached_step_function():
    
    if sys.version_info[:2] <= (2, 5):
        raise nose.SkipTest("Python 2.5 doesn't use `__instancecheck__`.")
    
    def my_step(state):
        raise NotImplementedError()
    
    assert not hasattr(my_step, '_BaseStepType__step_type')
    
    assert isinstance(my_step, BaseStep)
    
    
    assert hasattr(my_step, '_BaseStepType__step_type')
    
    assert isinstance(my_step, step_types_module.SimpleStep)
     
        
def test_uncached_step_function_25():
    
    def my_step(state):
        raise NotImplementedError()
    
    assert not hasattr(my_step, '_BaseStepType__step_type')
    
    assert BaseStep.__instancecheck__(my_step)
    
    
    assert hasattr(my_step, '_BaseStepType__step_type')
    
    assert step_types_module.SimpleStep.__instancecheck__(my_step)