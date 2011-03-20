# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Client` class.

See its documentation for more information.
'''

from garlicsim.general_misc import identities

import garlicsim


class Client(identities.HasIdentity):
    '''A client which needs to be served in a facility.'''
    def __init__(self):
        identities.HasIdentity.__init__(self)

        

