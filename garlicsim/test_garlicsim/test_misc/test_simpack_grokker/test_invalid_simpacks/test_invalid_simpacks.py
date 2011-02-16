# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for invalid simpacks.'''

from __future__ import with_statement

import os

import nose

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import cute_testing
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
    # sub-folders in the `simpacks` folder:
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
    
    with cute_testing.RaiseAssertor(type(exception_we_should_get),
                                    exception_we_should_get.message,
                                    assert_exact_type=True):
        
        SimpackGrokker(simpack)