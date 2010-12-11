# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the DontCopyPersistent class.

See its documentation for more information.
'''

from garlicsim.general_misc.copy_mode import CopyMode

class DontCopyPersistent(CopyMode):
    '''
    A copy mode under which Persistent objects aren't actually copied.
    
    When a Persistent is getting deepcopied with this mode, a reference to the
    original object would be returned instead of actually deepcopying it.
    
    Keep in mind that if the Persistent holds reference to additional objects,
    they too will not really be copied under this mode.
    '''

