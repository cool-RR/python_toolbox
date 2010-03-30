# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''

import pkg_resources
import wx
from garlicsim_wx.general_misc.third_party import aui

import garlicsim
from garlicsim_wx.widgets import WorkspaceWidget

from . import images as __images_package
images_package = __images_package.__name__


class PlaybackControls(wx.Panel, WorkspaceWidget):
    
    def __init__(self, frame):
        wx.Panel.__init__(self, frame, -1, size=(180, 96),
                               style=wx.SUNKEN_BORDER)
        aui_pane_info = aui.AuiPaneInfo().\
            Caption('PLAYBACK CONTROLS').\
            CloseButton(False).BestSize(180, 96).MinSize(180, 96).MaxSize(180, 96)
        WorkspaceWidget.__init__(self, frame, aui_pane_info)
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        
        
        bitmap_list = ['to_start', 'previous_node', 'play',
                                'next_node', 'to_end', 'pause',
                                'finalize']
        
        bitmaps_dict = self.bitmap_dict = {}
        for bitmap_name in bitmap_list:
            path = pkg_resources.resource_filename(images_package,
                                                   bitmap_name + '.png')
            self.bitmap_dict[bitmap_name] = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)

            
        """
        h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.plain = empty = wx.RadioButton(self, -1, 'Plain', style=wx.RB_GROUP)
        self.random = random = wx.RadioButton(self, -1, 'Random')
        random.SetValue(True)
        h_sizer1.Add(empty, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        h_sizer1.Add(random, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        v_sizer = wx.BoxSizer(wx.VERTICAL)

        last_h_sizer = wx.StdDialogButtonSizer()
        ok = wx.Button(self, wx.ID_OK, 'Ok', size=(70, 30))
        ok.SetDefault()
        last_h_sizer.SetAffirmativeButton(ok)
        cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(70, 30))
        last_h_sizer.AddButton(ok)
        last_h_sizer.AddButton(cancel)
        last_h_sizer.Realize()

        v_sizer.Add(h_sizer1, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        v_sizer.Add(last_h_sizer, 1, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(v_sizer)
        v_sizer.Fit(self)
        ok.SetFocus()
        """
        
        x = panel = wx.Panel(self, -1)

        v_sizer = self.v_sizer = wx.BoxSizer(wx.VERTICAL)

        '''h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(x, -1, 'Class Name')
        st1.SetFont(font)
        h_sizer1.Add(st1, 0, wx.RIGHT, 8)
        tc = wx.TextCtrl(x, -1)
        h_sizer1.Add(tc, 1)'''
        b1 = wx.Button(x, -1, size=(180, 30))
        v_sizer.Add(b1, 0, wx.EXPAND)


        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
                           
        self.button_to_start = wx.BitmapButton(
            x, -1, bitmaps_dict['to_start'], size=(30, 50)
        )
        self.button_previous_node = wx.BitmapButton(
            x, -1, bitmaps_dict['previous_node'], size=(30, 50)
        )
        self.button_play = wx.BitmapButton(
            x, -1, bitmaps_dict['play'], size=(60, 50)
        )
        self.button_next_node= wx.BitmapButton(
            x, -1, bitmaps_dict['next_node'], size=(30, 50)
        )
        self.button_to_end = wx.BitmapButton(
            x, -1, bitmaps_dict['to_end'], size=(30, 50)
        )
        
        
        button_line = (
            self.button_to_start,
            self.button_previous_node,
            self.button_play,
            self.button_next_node,
            self.button_to_end
        )
        
        for button in button_line:
            h_sizer.Add(button, 0)
        v_sizer.Add(h_sizer,)


        '''h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(x, -1, style=wx.TE_MULTILINE)'''
        b3 = wx.Button(x, -1, size=(180, 16))
        v_sizer.Add(b3, 1, wx.EXPAND)



        x.SetSizer(v_sizer)
        v_sizer.Fit(x)
        self.Centre()
        self.Show(True)
        
        
        '''
        v_sizer = self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        x = panel = wx.Panel(self, -1, )
        
        b1 = wx.Button(x, -1)
        b2 = wx.TextCtrl(x, size=(200, 200), style=wx.TE_MULTILINE)
        b3 = wx.Button(x, -1)
        
        v_sizer.Add(b1, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        v_sizer.Add(b2, 3, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        v_sizer.Add(b3, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        
        
        
        
        
        x.SetSizer(v_sizer)
        v_sizer.Fit(x)
        x.Centre()'''


    def on_size(self, e=None):
        self.Refresh()