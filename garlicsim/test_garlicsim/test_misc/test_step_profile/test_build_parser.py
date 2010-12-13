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
    
    
    different_step_profile = parse(4, 5, 6, meow='frrr')
    assert different_step_profile == parse(a=4, c=6, b=5, meow='frrr', **{})
    assert different_step_profile == parse(different_step_profile)
    assert different_step_profile == parse(step_profile=different_step_profile)
    
    assert different_step_profile != step_profile
    

    alternate_step_profile = alternate_parse()
    assert alternate_step_profile == alternate_parse(z=3) == \
           alternate_parse(1, y=2)
    
    assert none_parse(step_profile) == step_profile
    assert none_parse(step_profile=step_profile) == step_profile
    assert none_parse(different_step_profile) == different_step_profile
    assert none_parse(step_profile.step_function) == step_profile
    assert none_parse(step_function=alternate_step_profile.step_function) == \
           alternate_step_profile
    
    # blocktodo: make this test complete
    
    # Step function or step profile must be given to `none_parse`:
    nose.assert_raises(
        Exception,
        lambda: none_parse(1, 2, 3, 4, 5)
    )
    
    
    
    
    