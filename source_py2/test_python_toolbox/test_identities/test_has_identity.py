# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `identities.HasIdentity`.'''

import copy
import pickle

from python_toolbox import identities


class A(identities.HasIdentity):
    pass


def test_has_identity():
    '''Test the basic workings of `HasIdentity`.'''
    
    x0 = A()
    y0 = A()
    z0 = A()
    
    assert x0.has_same_identity_as(x0)
    assert y0.has_same_identity_as(y0)
    assert z0.has_same_identity_as(z0)
    
    assert x0 & x0
    assert y0 & y0
    assert z0 & z0
    
    assert not x0.has_same_identity_as(y0)
    assert not y0.has_same_identity_as(x0)
    assert not x0.has_same_identity_as(z0)
    assert not z0.has_same_identity_as(x0)
    assert not y0.has_same_identity_as(z0)
    assert not z0.has_same_identity_as(y0)
    
    assert not x0 & y0
    assert not y0 & x0
    assert not x0 & z0
    assert not z0 & x0
    assert not y0 & z0
    assert not z0 & y0
    
    ### Testing deepcopies: ###################################################
    #                                                                         #
    x1 = copy.deepcopy(x0)
    y1 = copy.deepcopy(y0)
    z1 = copy.deepcopy(z0)
    
    assert x0 & x1
    assert y0 & y1
    assert z0 & z1
    
    assert x0.has_same_identity_as(x1)
    assert x1.has_same_identity_as(x0)
    assert y0.has_same_identity_as(y1)
    assert y1.has_same_identity_as(y0)
    assert z0.has_same_identity_as(z1)
    assert z1.has_same_identity_as(z0)
    #                                                                         #
    ### Finished testing deepcopies. ##########################################
    
    ### Testing picked-unpickled copies: ######################################
    #                                                                         #
    x2 = pickle.loads(pickle.dumps(x0, protocol=2))
    y2 = pickle.loads(pickle.dumps(y0, protocol=2))
    z2 = pickle.loads(pickle.dumps(z0, protocol=2))
    
    assert x2 & x1
    assert y2 & y1
    assert z2 & z1
    
    assert x2.has_same_identity_as(x1)
    assert x1.has_same_identity_as(x2)
    assert y2.has_same_identity_as(y1)
    assert y1.has_same_identity_as(y2)
    assert z2.has_same_identity_as(z1)
    assert z1.has_same_identity_as(z2)
    #                                                                         #
    ### Finished testing picked-unpickled copies. #############################

    