# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import os

import nose

from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import path_tools

import garlicsim
from garlicsim.misc.simpack_grokker import SimpackGrokker, Settings
from garlicsim.misc.simpack_grokker.step_type import StepType, BaseStep

import test_garlicsim


def test_simpacks():
    from . import simpacks as simpacks_package
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(simpacks_package).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `simpacks` folder:
    simpacks_dir = os.path.dirname(simpacks_package.__file__)
    assert len(path_tools.list_sub_folders(simpacks_dir)) == \
           len(simpacks)
    
    for simpack in simpacks:
        test_garlicsim.verify_simpack_settings(simpack)
        yield check_simpack, simpack

        
def check_simpack(simpack):

    _test_settings = simpack._test_settings
    
    simpack_grokker = SimpackGrokker(simpack)
    

    # Test the caching:
    assert simpack_grokker is SimpackGrokker(simpack)

    
    step_profile = simpack_grokker.build_step_profile()
    assert step_profile.function == simpack_grokker.default_step_function
    assert isinstance(step_profile, garlicsim.misc.StepProfile)
    assert (not step_profile.args) and (not step_profile.kwargs)

    
    assert len(simpack_grokker.all_step_functions) == \
           _test_settings.N_STEP_FUNCTIONS 

    
    state = simpack.State.create_root()
    assert SimpackGrokker.create_from_state(state) is simpack_grokker

    
    assert simpack_grokker.available_cruncher_types == \
           simpack._test_settings.CRUNCHERS_LIST
    assert simpack_grokker.available_cruncher_types == \
           [cruncher for cruncher, availability in 
            simpack_grokker.cruncher_types_availability.items()
            if availability]    
    assert all(        
        issubclass(cruncher, garlicsim.asynchronous_crunching.BaseCruncher)
        for cruncher in simpack_grokker.cruncher_types_availability.keys()
    )

    
    assert simpack_grokker.default_step_function == \
           _test_settings.DEFAULT_STEP_FUNCTION
    
    
    assert simpack_grokker.history_dependent == \
           _test_settings.HISTORY_DEPENDENT

    
    settings = simpack_grokker.settings
    assert isinstance(settings, Settings)
    assert callable(settings.DETERMINISM_FUNCTION)

    
    if not simpack_grokker.history_dependent:
        assert isinstance(simpack_grokker.step(state, step_profile),
                          simpack.State)        
        iterator = simpack_grokker.get_step_iterator(state, step_profile)
        assert iterator.__iter__() is iterator

    
    step_types = simpack_grokker.step_functions_by_type.keys()
    assert all(issubclass(step_type, BaseStep) for step_type in step_types)
    
    # Fetched in a different way than `simpack_grokker.all_step_functions`:
    all_step_functions = sequence_tools.flatten(
        simpack_grokker.step_functions_by_type.values()
    )
    assert all(
        issubclass(StepType.get_step_type(step_function), BaseStep) for
        step_function in all_step_functions
    )
    assert len(all_step_functions) == _test_settings.N_STEP_FUNCTIONS
    
    
    
    

    
    