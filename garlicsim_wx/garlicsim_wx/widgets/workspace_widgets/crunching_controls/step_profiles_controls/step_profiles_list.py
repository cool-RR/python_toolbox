# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx
from garlicsim_wx.general_misc.third_party import hypertreelist

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget

    
class StepProfilesList(hypertreelist.HyperTreeList):
    '''tododoc'''
    # tododoc: set max size dynamically according to number of profiles
    
    def __init__(self, parent, frame):
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        
        hypertreelist.HyperTreeList.__init__(
            self,
            parent,
            style=wx.SIMPLE_BORDER,
            agwStyle=(
                wx.TR_FULL_ROW_HIGHLIGHT | \
                wx.TR_ROW_LINES | \
                wx.TR_HIDE_ROOT | \
                hypertreelist.TR_NO_HEADER
                )
        )        
        
        self.AddColumn('')
        self.SetMainColumn(0)
        self.root_item = self.AddRoot('')
        
        self.static_text = wx.StaticText(self, -1, 'boobies')
        
        self.AppendItem(self.root_item, 'boobs', ct_type=1, wnd=self.static_text)
        self.AppendItem(self.root_item, 'ass', ct_type=2, wnd=None)
        self.AppendItem(self.root_item, 'tits', ct_type=2, wnd=None)