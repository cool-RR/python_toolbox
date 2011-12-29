# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import nose.tools

import garlicsim
from garlicsim.asynchronous_crunching.crunchers import PiCloudCruncher


def test_pi_cloud_cruncher():
    '''Test the `PiCloudCruncher` placeholder.'''
    # Allowing either `TypeError` or `NotImplementedError`:
    try:
        nose.tools.assert_raises(TypeError, PiCloudCruncher)
    except Exception:
        nose.tools.assert_raises(NotImplementedError, PiCloudCruncher)
    
        
    from test_garlicsim.test_misc.test_simpack_grokker.simpacks import simpack
    simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    availability = \
        PiCloudCruncher.can_be_used_with_simpack_grokker(simpack_grokker)
    assert availability == False