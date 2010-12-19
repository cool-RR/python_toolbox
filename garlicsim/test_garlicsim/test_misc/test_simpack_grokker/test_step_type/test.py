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