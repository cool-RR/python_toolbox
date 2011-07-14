# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StateCreationDialog` class.

See its documentation for more info.
'''

import random
import warnings
import functools

import wx

from garlicsim_wx.widgets.general_misc.cute_error_dialog import CuteErrorDialog
import garlicsim_wx.widgets.misc.default_state_creation_dialog
import garlicsim.data_structures


class StateCreationDialog(garlicsim_wx.widgets.misc.BaseStateCreationDialog):
    '''Initial dialog for creating a root state.'''
    
    def __init__(self, frame):
        garlicsim_wx.widgets.misc.BaseStateCreationDialog.__init__(
            self,
            frame,
            title='Creating a root state'
        )
        
        self.frame = frame
        self.simpack = frame.gui_project.simpack

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        width_help_text = 'Set the width of the Life board, in cells.'
        
        self.x_title = x_title = wx.StaticText(self, -1, '&Width: ')
        hbox1.Add(
            x_title,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.TOP | wx.LEFT,
            5)
        
        self.x_textctrl = x_textctrl = wx.TextCtrl(self, -1, '45')
        hbox1.Add(x_textctrl, 0, wx.EXPAND | wx.ALL, 5)
        
        self.x_title.SetHelpText(width_help_text)
        self.x_textctrl.SetHelpText(width_help_text)
        self.x_title.SetToolTipString(width_help_text)
        self.x_textctrl.SetToolTipString(width_help_text)
        
        hbox1.AddSpacer(30)
        
        height_help_text = 'Set the height of the Life board, in cells.'
        
        self.y_title = y_title = wx.StaticText(self, -1, '&Height: ')
        hbox1.Add(
            y_title,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.TOP | wx.LEFT,
            5
        )
        self.y_textctrl = y_textctrl = wx.TextCtrl(self, -1, '25')
        hbox1.Add(y_textctrl, 0, wx.EXPAND | wx.ALL, 5)
        
        self.y_title.SetHelpText(height_help_text)
        self.y_textctrl.SetHelpText(height_help_text)
        self.y_title.SetToolTipString(height_help_text)
        self.y_textctrl.SetToolTipString(height_help_text)

        
        ### Building radio buttons for fill option: ###########################
        #                                                                     #
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.empty_radio_button = wx.RadioButton(self, -1, 'All &empty',
                                                 style=wx.RB_GROUP)
        empty_help_text = ('All the cells in the board will be empty, '
                           'i.e. dead.')
        self.empty_radio_button.SetHelpText(empty_help_text)
        self.empty_radio_button.SetToolTipString(empty_help_text)
        
        self.full_radio_button = wx.RadioButton(self, -1, 'All &full')
        full_help_text = ('All the cells in the board will be full, '
                          'i.e. alive.')
        self.full_radio_button.SetHelpText(full_help_text)
        self.full_radio_button.SetToolTipString(full_help_text)
        
        self.random_radio_button = wx.RadioButton(self, -1, '&Random')
        random_help_text = ('The board will be a random mixture of live '
                            'cells and dead cells.')
        self.random_radio_button.SetHelpText(random_help_text)
        self.random_radio_button.SetToolTipString(random_help_text)
        
        self.random_radio_button.SetValue(True)
        
        hbox2.Add(self.empty_radio_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbox2.Add(self.full_radio_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbox2.Add(self.random_radio_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        #                                                                     #
        ### Finished building radio buttons for fill option. ##################
        
        vbox = wx.BoxSizer(wx.VERTICAL)

        last_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, wx.ID_OK, 'Create &state')
        ok_help_text = 'Create the new state.'
        self.ok_button.SetHelpText(ok_help_text)
        self.ok_button.SetToolTipString(ok_help_text)
        self.ok_button.SetDefault()
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        last_hbox.Add(self.ok_button, 0)
        last_hbox.Add(self.cancel_button, 0, wx.LEFT, 5)

        vbox.Add(hbox1, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(hbox2, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(last_hbox, 1, wx.ALIGN_CENTER |  wx.BOTTOM, 10)
        
        self.bind_event_handlers(StateCreationDialog)

        self.SetSizer(vbox)
        vbox.Fit(self)
        self.ok_button.SetFocus()

        
    def _on_ok_button(self, event):
        try:
            width = int(self.x_textctrl.GetValue())
        except ValueError:
            CuteErrorDialog.create_and_show_modal(self, 'Bad width!')
            return

        try:
            height = int(self.y_textctrl.GetValue())
        except ValueError:
            CuteErrorDialog.create_and_show_modal(self, 'Bad height!')
            return

        fill = 'full' if self.full_radio_button.GetValue() else \
            'empty' if self.empty_radio_button.GetValue() else 'random'
        
        self.state = self.simpack.State.create_root(width, height, fill)

        self.EndModal(wx.ID_OK)

        
    def _on_cancel_button(self, event):
        self.EndModal(wx.ID_CANCEL)
        

