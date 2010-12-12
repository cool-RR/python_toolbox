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
    from . import sample_problematic_simpacks
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(sample_problematic_simpacks).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `sample_problematic_simpacks` folders:
    sample_problematic_simpacks_dir = \
        os.path.dirname(sample_problematic_simpacks.__file__)
    assert len(
        path_tools.list_sub_folders(sample_problematic_simpacks_dir)
        ) == len(simpacks)
    
    for simpack in simpacks:
        test_garlicsim.verify_sample_simpack_settings(simpack)
        yield check_simpack, simpack

        
def check_simpack(simpack):

    _settings_for_testing = simpack._settings_for_testing
    PROBLEM = _settings_for_testing.PROBLEM
    assert PROBLEM
    assert issubclass(PROBLEM, Exception)
    
    try:
        SimpackGrokker(simpack)
    except Exception, exception:
        assert type(exception) is PROBLEM
        
    else:
        raise Exception("`SimpackGrokker` shouldn't have been created because "
                        "the simpack is problematic.")