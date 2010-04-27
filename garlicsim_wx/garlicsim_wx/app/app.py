# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the App class.

See its documentation for more information.
'''

import wx

import garlicsim_wx


class App(wx.PySimpleApp):
    # todo: need to think if i allow frames with no app. on one hand good idea,
    # to allow people to start a garlicsim_wx frame in their own app. on other
    # hand frames will need to know how to start another frame.
    def __init__(self, new_gui_project=False, load_gui_project=None):
        self.frame = None
        assert not (new_gui_project and load_gui_project)
        self.new_gui_project = new_gui_project
        self.load_gui_project = load_gui_project
        super(App, self).__init__()
        
    
    def OnInit(self):
        
        frame = garlicsim_wx.Frame(
            parent=None,
            title="GarlicSim",
            size=(1140, 850)
        )
        
        self.frame = frame
        
        self.SetTopWindow(frame)
        
        if self.new_gui_project is True:
            wx.CallAfter(frame.on_new)
        
        return True