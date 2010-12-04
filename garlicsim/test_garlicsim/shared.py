from garlicsim.general_misc import import_tools

import garlicsim


def verify_sample_simpack_settings(sample_simpack):
    import_tools.import_all(sample_simpack)
    sft = sample_simpack._settings_for_testing
    assert isinstance(sft.ENDABLE, bool)
    assert isinstance(sft.HISTORY_DEPENDENT, bool)
    assert isinstance(sft.N_STEP_FUNCTIONS, int)
    assert callable(sft.DEFAULT_STEP_FUNCTION)
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