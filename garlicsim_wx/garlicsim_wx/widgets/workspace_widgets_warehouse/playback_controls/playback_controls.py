# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''

import pkg_resources
import wx

import garlicsim
from garlicsim_wx.widgets import WorkspaceWidget

from . import images as __images_package
images_package = __images_package.__name__


class PlaybackControls(wx.Panel, WorkspaceWidget):
    
    def __init__(self, frame):
        wx.Panel.__init__(self, frame, size=(500, 500),
                               style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        
        panel = wx.Panel(self, -1)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, -1, 'Class Name')
        st1.SetFont(font)
        hbox1.Add(st1, 0, wx.RIGHT, 8)
        tc = wx.TextCtrl(panel, -1)
        hbox1.Add(tc, 1)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, -1, 'Matching Classes')
        st2.SetFont(font)
        hbox2.Add(st2, 0)
        vbox.Add(hbox2, 0, wx.LEFT | wx.TOP, 10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
        hbox3.Add(tc2, 1, wx.EXPAND)
        vbox.Add(hbox3, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, -1, 'Case Sensitive')
        cb1.SetFont(font)
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, -1, 'Nested Classes')
        cb2.SetFont(font)
        hbox4.Add(cb2, 0, wx.LEFT, 10)
        cb3 = wx.CheckBox(panel, -1, 'Non-Project classes')
        cb3.SetFont(font)
        hbox4.Add(cb3, 0, wx.LEFT, 10)
        vbox.Add(hbox4, 0, wx.LEFT, 10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, -1, 'Ok', size=(70, 30))
        hbox5.Add(btn1, 0)
        btn2 = wx.Button(panel, -1, 'Close', size=(70, 30))
        hbox5.Add(btn2, 0, wx.LEFT | wx.BOTTOM , 5)
        vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

        panel.SetSizer(vbox)
        vbox.Fit(panel)
        self.Centre()
        self.Show(True)
        
        """v_sizer = self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetBackgroundColour('#4f5049')


        midPan = wx.Panel(self, -1)
        midPan.SetBackgroundColour('#ededed')
        
        
        '''
        b1 = wx.Button(self, -1)
        b2 = wx.TextCtrl(self, size=(200, 200), style=wx.TE_MULTILINE)
        b3 = wx.Button(self, -1)
        
        v_sizer.Add(b1, 1, wx.EXPAND)# | wx.ALIGN_CENTER_HORIZONTAL)
        v_sizer.Add(b2, 1, wx.EXPAND)# | wx.ALIGN_CENTER_HORIZONTAL)
        v_sizer.Add(b3, 1, wx.EXPAND)# | wx.ALIGN_CENTER_HORIZONTAL)
        '''
        
        v_sizer.Add(midPan, 1, wx.EXPAND | wx.ALL, 20)
        
        
        midPan2 = wx.Panel(self, -1)
        midPan2.SetBackgroundColour('#00ff22')
        
        v_sizer.Add(midPan2, 1, wx.EXPAND | wx.ALL, 20)
        
        self.SetSizer(v_sizer)
        v_sizer.Fit(self)
        self.Centre()"""


    def on_size(self, e=None):
        self.Refresh()