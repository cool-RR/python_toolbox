import os

import nose

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc.reasoned_bool import ReasonedBool

import garlicsim
from garlicsim.misc.simpack_grokker import SimpackGrokker
from garlicsim.misc.exceptions import InvalidSimpack

import test_garlicsim


def test_simpacks():
    from . import sample_invalid_simpacks
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(sample_invalid_simpacks).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `sample_invalid_simpacks` folders:
    sample_invalid_simpacks_dir = \
        os.path.dirname(sample_invalid_simpacks.__file__)
    assert len(path_tools.list_sub_folders(sample_invalid_simpacks_dir)) == \
           len(simpacks)
    
    for simpack in simpacks:
        test_garlicsim.verify_sample_simpack_settings(simpack)
        yield check_simpack, simpack

        
def check_simpack(simpack):

    _settings_for_testing = simpack._settings_for_testing
    PROBLEM = None
VALID = _settings_for_testing.VALID
    assert not VALID
    assert isinstance(VALID, ReasonedBool)
    exception_we_should_get = VALID.reason
    assert isinstance(exception_we_should_get, InvalidSimpack)
    
    try:
        SimpackGrokker(simpack)
    except Exception, exception:
        assert type(exception) == type(exception_we_should_get)
        assert exception.message == exception_we_should_get.message
        
    else:
        raise Exception("`SimpackGrokker` shouldn't have been created because "
                        "the simpack is invalid.")