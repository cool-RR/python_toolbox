# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DefaultStateCreationDialog` class.

See its documentation for more info.
'''

import wx

from .base_state_creation_dialog import BaseStateCreationDialog


class DefaultStateCreationDialog(BaseStateCreationDialog):
    '''
    An initial dialog to show when creating a root state.
    
    This is a generic one, used if the simpack doesn't define its own.
    '''
    def __init__(self, frame):
   
        BaseStateCreationDialog.__init__(self,
                                     frame,
                                     title='Creating a root state')
        
        self.frame = frame
        self.simpack = frame.gui_project.simpack
        State = self.simpack.State

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.messy_check_box = messy_check_box = \
                                                wx.CheckBox(self, -1, '&Messy')
        messy_help_text = ('Create a messy chaotic state with lots of '
                           'interesting features. Useful for test-driving the '
                           'simpack.')
        messy_check_box.SetValue(True)
        if State.create_root is None or State.create_messy_root is None:
            messy_check_box.Disable()
            if State.create_messy_root is None:
                messy_check_box.SetValue(False)
                messy_help_text += (" Not available because the simpack "
                                    "doesn't define `create_messy_root`.")
            else:
                messy_help_text += (" Can't be canceled because the simpack "
                                    "doesn't define `create_root`.")
        messy_check_box.SetToolTipString(messy_help_text)
        messy_check_box.SetHelpText(messy_help_text)
        
        vbox.Add(messy_check_box, 0, wx.ALL, 10)
        
        # todo: add slick way to add args/kwargs

        last_hbox = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK, 'Create &state')
        ok_help_text = 'Create the new state.'
        self.ok_button.SetToolTipString(ok_help_text)
        self.ok_button.SetHelpText(ok_help_text)
        self.ok_button.SetDefault()
        last_hbox.SetAffirmativeButton(self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        last_hbox.AddButton(self.ok_button)
        last_hbox.AddButton(self.cancel_button)
        last_hbox.Realize()

        vbox.Add(last_hbox, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(vbox)
        vbox.Fit(self)
        self.ok_button.SetFocus()
        
        self.bind_event_handlers(DefaultStateCreationDialog)

        
    ### Event handlers: #######################################################
    #                                                                         #
    def _on_ok_button(self, event):
        self.state = self.simpack.State.create_messy_root() if \
            self.messy_check_box.Value is True else \
            self.simpack.State.create_root()
        self.EndModal(wx.ID_OK)
        
        
    def _on_cancel_button(self, event):
        self.EndModal(wx.ID_CANCEL)
    #                                                                         #
    ### Finished event handlers. ##############################################

        
        