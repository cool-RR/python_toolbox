# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for invalid simpacks.'''

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
    '''Test invalid simpacks.'''
    from . import simpacks as invalid_simpacks_package
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(invalid_simpacks_package).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `invalid_simpacks_package` folders:
    simpacks_dir = \
        os.path.dirname(invalid_simpacks_package.__file__)
    assert len(path_tools.list_sub_folders(simpacks_dir)) == \
           len(simpacks)
    
    for simpack in simpacks:
        test_garlicsim.verify_simpack_settings(simpack)
        yield check_simpack, simpack

        
def check_simpack(simpack):
    '''Check that the invalid `simpack` raises the correct exception.'''
    _test_settings = simpack._test_settings
    VALID = _test_settings.VALID
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