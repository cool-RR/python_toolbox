# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the StateCreationDialog class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.widgets.general_misc import CuteDialog


class StateCreationDialog(CuteDialog): # make base class
    '''
    An initial dialog to show when creating a root state.
    
    This is a generic one, used if the simpack doesn't define its own.
    '''
    def __init__(self, frame):
   
        CuteDialog.__init__(self, frame, title='Creating a root state')
        
        self.frame = frame
        self.simpack = frame.gui_project.simpack
        State = self.simpack.State

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.messy_check_box = messy_check_box = wx.CheckBox(self, -1, 'Messy' )
        tool_tip_string = '''Make a messy chaotic state, useful for \
test-driving the simpack.'''
        messy_check_box.SetValue(True)
        if State.create_root is None or State.create_messy_root is None:
            messy_check_box.Disable()
            if State.create_messy_root is None:
                messy_check_box.SetValue(False)
                tool_tip_string += ''' Not available because the simpack \
doesn't define `create_messy_root`.'''
            else:
                tool_tip_string += ''' Can't be canceled because the simpack \
doesn't define `create_root`.'''
        messy_check_box.SetToolTipString(tool_tip_string)
        
        vbox.Add(messy_check_box, 0, wx.ALL, 10)
        
        # todo: add slick way to add args/kwargs

        last_hbox = wx.StdDialogButtonSizer()
        ok = wx.Button(self, wx.ID_OK, 'Ok', size=(70, 30))
        ok.SetDefault()
        last_hbox.SetAffirmativeButton(ok)
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=ok.GetId())
        cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.on_cancel, id=cancel.GetId())
        last_hbox.AddButton(ok)
        last_hbox.AddButton(cancel)
        last_hbox.Realize()

        vbox.Add(last_hbox, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(vbox)
        vbox.Fit(self)
        ok.SetFocus()

        
    def start(self):
        '''Start the dialog to make a new state.'''
        if self.ShowModal() == wx.ID_OK:
            creator = self.simpack.State.create_messy_root if \
                    self.messy_check_box.GetValue() is True else \
                    self.simpack.State.create_root
            
            state = creator()
        else:
            state = None
        self.Destroy()
        return state

    
    def on_ok(self, event):
        '''Do 'Okay' on the dialog.'''

        self.EndModal(wx.ID_OK)

        
        
    def on_cancel(self, event):
        '''Do 'cancel' on the dialog'''
        
        self.EndModal(wx.ID_CANCEL)

        
        