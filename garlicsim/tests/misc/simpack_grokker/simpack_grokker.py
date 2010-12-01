import nose

from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc import import_tools

import garlicsim
from garlicsim.misc.simpack_grokker import (SimpackGrokker, Settings,
                                            get_step_type)
from garlicsim.misc.simpack_grokker.base_step_type import BaseStepType


def test_simpacks():
    from . import sample_simpacks
    simpacks = import_tools.import_all(sample_simpacks)
    for simpack in simpacks:
        # Making `_settings_for_testing` available:
        import_tools.import_all(simpack)
        yield check_simpack, simpack

        
def check_simpack(simpack):

    _settings_for_testing = simpack._settings_for_testing
    
    simpack_grokker = SimpackGrokker(simpack)
    

    # Test the caching:
    assert simpack_grokker is SimpackGrokker(simpack)

    
    step_profile = simpack_grokker.build_step_profile()
    assert step_profile.function == simpack_grokker.default_step_function
    assert isinstance(step_profile, garlicsim.misc.StepProfile)
    assert (not step_profile.args) and (not step_profile.kwargs)

    
    assert len(simpack_grokker.all_step_functions) == \
           _settings_for_testing.N_STEP_FUNCTIONS 

    
    state = simpack.State.create_root()
    assert SimpackGrokker.create_from_state(state) is simpack_grokker

    
    assert simpack_grokker.available_cruncher_types == \
           [cruncher for cruncher, availability in 
            simpack_grokker.cruncher_types_availability.items()
            if availability]    
    assert all(        
        issubclass(cruncher, garlicsim.asynchronous_crunching.BaseCruncher)
        for cruncher in simpack_grokker.cruncher_types_availability.keys()
    )

    
    assert simpack_grokker.default_step_function == \
           _settings_for_testing.DEFAULT_STEP_FUNCTION

    
    nose.tools.assert_raises(NotImplementedError,
                             simpack_grokker.get_inplace_step_iterator,
                             state,
                             step_profile)

    
    iterator = simpack_grokker.get_step_iterator(state, step_profile)
    assert iterator.__iter__() is iterator
    # tododoc: make separate tests for iterator

    
    assert simpack_grokker.history_dependent == \
           _settings_for_testing.HISTORY_DEPENDENT

    
    settings = simpack_grokker.settings
    assert isinstance(settings, Settings)
    assert callable(settings.DETERMINISM_FUNCTION)

    
    assert isinstance(simpack_grokker.step(state, step_profile), simpack.State)

    
    step_types = simpack_grokker.step_functions_by_type.keys()
    assert all(issubclass(step_type, BaseStepType) for step_type in step_types)
    
    # Fetched in a different way than `simpack_grokker.all_step_functions`:
    all_step_functions = sequence_tools.flatten(
        simpack_grokker.step_functions_by_type.values()
    )
    assert all(
        issubclass(get_step_type(step_function), BaseStepType) for 
        step_function in all_step_functions
    )
    assert len(all_step_functions) == _settings_for_testing.N_STEP_FUNCTIONS
    
    
    
    

    
    