# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Client` class.

See its documentation for more information.
'''

import garlicsim


class Client(object):
    '''A client which needs to be served in the facility.'''
    def __init__(self):
        self.identity = \
            garlicsim.general_misc.persistent.CrossProcessPersistent()

        

