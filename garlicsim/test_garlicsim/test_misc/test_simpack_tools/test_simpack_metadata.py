# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing package for `garlicsim.misc.simpack_tools.SimpackMetadata`.'''

import copy
import pickle
import cPickle

from garlicsim.misc.simpack_tools import SimpackMetadata


def test_class_pickling():
    assert SimpackMetadata is copy.deepcopy(SimpackMetadata)
    assert SimpackMetadata is pickle.loads(pickle.dumps(SimpackMetadata))
    assert SimpackMetadata is cPickle.loads(cPickle.dumps(SimpackMetadata))
    

def test_on_garlicsim_lib():
    simpack_names = ('life', 'prisoner', 'queue')
    prefix = 'garlicsim_lib.simpacks.'
    
    addresses = [(prefix + simpack_name) for simpack_name in simpack_names]
    for address in addresses:
        simpack_metadata = SimpackMetadata.create_from_address(address)