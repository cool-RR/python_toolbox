import garlicsim
from garlicsim.misc import StepProfile

from ..test_simpack_grokker.sample_simpacks import simpack


def test():
    simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    parse_arguments_to_step_profile = StepProfile.build_parser(
        simpack_grokker.default_step_function
    )
    
    parse_arguments_to_step_profile(