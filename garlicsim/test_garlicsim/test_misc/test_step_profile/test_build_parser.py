import nose

import garlicsim

from garlicsim.misc import StepProfile

from . import sample_simpack


def test():
    simpack_grokker = garlicsim.misc.SimpackGrokker(sample_simpack)
    
    parse = \
        StepProfile.build_parser(sample_simpack.State.step)
    alternate_parse = \
        StepProfile.build_parser(sample_simpack.State.alternate_step)
    none_parse = \
        StepProfile.build_parser(None)
    
    
    default_step_profile = parse()
    
    step_profile = parse(1, 2, 3)
    assert step_profile == default_step_profile == StepProfile(
        sample_simpack.State.step,
        1, 2, 3
    )
    assert step_profile == alternate_parse(step_profile) == none_parse(step_profile) == alternate_parse(step_profile=step_profile)
    
    
    different_step_profile = parse(4, 5, 6)
    assert different_step_profile == parse(a=4, c=6, b=5)
    assert different_step_profile == parse(different_step_profile)
    assert different_step_profile == parse(step_profile=different_step_profile)
    
    assert different_step_profile != step_profile
    
    

    
    
    
    
    
    
    
    
    
    
    
    