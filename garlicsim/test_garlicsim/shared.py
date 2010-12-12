from garlicsim.general_misc import import_tools

import garlicsim


def verify_sample_simpack_settings(sample_simpack):
    __import__(sample_simpack.__name__ + '._settings_for_testing')
    sft = sample_simpack._settings_for_testing
    assert isinstance(sft.ENDABLE, bool)
    bool(sft.VALID)
    assert (sft.PROBLEM is None) or issubclass(sft.PROBLEM, Exception)
    assert isinstance(sft.HISTORY_DEPENDENT, bool)
    assert isinstance(sft.N_STEP_FUNCTIONS, int)
    if sft.DEFAULT_STEP_FUNCTION is not None:
        assert callable(sft.DEFAULT_STEP_FUNCTION)
    if sft.DEFAULT_STEP_FUNCTION_TYPE is not None:
        assert issubclass(
            sft.DEFAULT_STEP_FUNCTION_TYPE,
            garlicsim.misc.simpack_grokker.base_step_type.BaseStepType
        )
    assert isinstance(sft.CONSTANT_CLOCK_INTERVAL, int) or \
           sft.CONSTANT_CLOCK_INTERVAL is None
    assert isinstance(sft.CRUNCHERS_LIST, list)
    for cruncher_type in sft.CRUNCHERS_LIST:
        assert issubclass(cruncher_type,
                          garlicsim.asynchronous_crunching.BaseCruncher)
        
    # Making sure there aren't any extraneous settings, so we'll know we checked
    # everything:
    settings_names = [name for name in dir(sft) if name.isupper()]
    assert len(settings_names) == 9
