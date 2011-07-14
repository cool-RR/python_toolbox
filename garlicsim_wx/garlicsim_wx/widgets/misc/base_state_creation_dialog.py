# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BaseStateCreationDialog` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog


class BaseStateCreationDialog(CuteDialog):
    '''
    An initial dialog to show when creating a root state.
    
    This is a generic one, used if the simpack doesn't define its own.
    
    blocktododoc
    '''
    @classmethod
    def create_show_modal_and_get_state(cls, frame):
        state_creation_dialog = cls(frame)
        try:
            result = state_creation_dialog.ShowModal()
        finally:
            state_creation_dialog.Destroy()
        return state_creation_dialog.state if result == wx.ID_OK else None

        
        