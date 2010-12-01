import nose

import garlicsim
from garlicsim.misc.simpack_grokker import SimpackGrokker, Settings


def test():
    from .sample_simpacks import simpack
    
    simpack_grokker = SimpackGrokker(simpack)
    
    # Test the caching:
    assert simpack_grokker is SimpackGrokker(simpack)
    
    assert len(simpack_grokker.all_step_functions) == 1
    
    state = simpack.State.create_root()
    assert SimpackGrokker.create_from_state(state) is simpack_grokker
    
    assert simpack_grokker.available_cruncher_types == \
           [cruncher for cruncher, availability in 
            simpack_grokker.cruncher_types_availability.items()
            if availability]    
    assert all(        
        isinstance(cruncher, garlicsim.asynchronous_crunching.BaseCruncher)
        for cruncher in simpack_grokker.cruncher_types_availability.keys()
    )
    
    assert simpack_grokker.default_step_function == simpack.State.step
    
    nose.tools.assert_raises(NotImplementedError,
                             simpack_grokker.get_inplace_step_iterator)
    
    iterator = simpack_grokker.get_step_iterator()
    assert iterator.__iter__() is iterator
    # tododoc: make separate tests for iterator
    
    assert not simpack_grokker.history_dependent
    
    settings = simpack_grokker.settings
    assert isinstance(settings, Settings)
    assert callable(settings.DETERMINISM_FUNCTION)
    
    
    
    
    
    

    
    