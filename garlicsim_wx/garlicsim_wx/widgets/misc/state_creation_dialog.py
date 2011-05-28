# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StateCreationDialog` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog


class StateCreationDialog(CuteDialog): # make base class
    '''
    An initial dialog to show when creating a root state.
    
    This is a generic one, used if the simpack doesn't define its own.
    
    blocktododoc
    '''
    @classmethod
    def create_show_modal_and_get_state(cls, frame):
        dialog = cls(frame)
        try:
            result = dialog.ShowModal()
        finally:
            dialog.Destroy()
        return self.state if result == wx.ID_OK else None

        
        