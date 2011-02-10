# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for testing `garlicsim`.'''


from garlicsim.general_misc import import_tools

import garlicsim 


def verify_simpack_settings(sample_simpack):
    '''
    Verfiy that `sample_simpack` has all the testing flags with valid values.
    '''
    import_tools.normal_import(
        sample_simpack.__name__ + '._test_settings'
    )
    _test_settings = sample_simpack._test_settings
    assert isinstance(_test_settings.ENDABLE, bool)
    bool(_test_settings.VALID)
    assert (_test_settings.PROBLEM is None) or \
           issubclass(_test_settings.PROBLEM, Exception)
    assert isinstance(_test_settings.HISTORY_DEPENDENT, bool)
    assert isinstance(_test_settings.N_STEP_FUNCTIONS, int)
    if _test_settings.DEFAULT_STEP_FUNCTION is not None:
        assert callable(_test_settings.DEFAULT_STEP_FUNCTION)
    if _test_settings.DEFAULT_STEP_FUNCTION_TYPE is not None:
        assert issubclass(
            _test_settings.DEFAULT_STEP_FUNCTION_TYPE,
            garlicsim.misc.simpack_grokker.step_type.BaseStep
        )
    assert isinstance(_test_settings.CONSTANT_CLOCK_INTERVAL, int) or \
           _test_settings.CONSTANT_CLOCK_INTERVAL is None
    assert isinstance(_test_settings.CRUNCHERS_LIST, list)
    for cruncher_type in _test_settings.CRUNCHERS_LIST:
        assert issubclass(cruncher_type,
                          garlicsim.asynchronous_crunching.BaseCruncher)
        
    # Making sure there aren't any extraneous settings, so we'll know we
    # checked everything:
    settings_names = [name for name in dir(_test_settings) if name.isupper()]
    assert len(settings_names) == 9
