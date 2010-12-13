import nose.tools

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
    assert step_profile == \
           alternate_parse(step_profile) == \
           none_parse(step_profile) == \
           alternate_parse(step_profile=step_profile)
    
    assert parse(step_profile=None) == step_profile
    
    
    different_step_profile = parse(4, 5, 6, meow='frrr')
    assert different_step_profile == parse(a=4, c=6, b=5, meow='frrr', **{})
    assert different_step_profile == parse(different_step_profile)
    assert different_step_profile == parse(step_profile=different_step_profile)
    
    assert different_step_profile != step_profile
    
    
    

    alternate_step_profile = alternate_parse()
    assert alternate_step_profile == alternate_parse(z=3) == \
           alternate_parse(1, y=2)
    assert alternate_parse(step_profile.step_function, 4, 5, 6) == \
           alternate_parse(
               step_function=step_profile.step_function, a=4, b=5, c=6
               ) == \
           parse(4, 5, 6)
    assert alternate_parse(step_profile=step_profile) == step_profile
    
    assert none_parse(step_profile) == step_profile
    assert none_parse(step_profile=step_profile) == step_profile
    assert none_parse(different_step_profile) == different_step_profile
    assert none_parse(step_profile.step_function) == step_profile
    assert none_parse(step_function=alternate_step_profile.step_function) == \
           alternate_step_profile
    assert none_parse(alternate_step_profile.step_function, 2) == \
           alternate_parse(x=2)
    
    # Step function or step profile must be given to `none_parse`:
    nose.tools.assert_raises(
        Exception,
        lambda: none_parse(1, 2, 3, 4, 5)
    )
    
    # `alternate_step` doesn't take **kwargs:
    nose.tools.assert_raises(
        Exception,
        lambda: alternate_parse(boom='kaplaow')
    )