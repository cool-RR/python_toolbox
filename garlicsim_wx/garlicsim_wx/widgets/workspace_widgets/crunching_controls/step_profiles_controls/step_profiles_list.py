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
    
    def __init__(self, parent, frame, *args, **kwargs):
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        
        hypertreelist.HyperTreeList.__init__(
            self,
            parent,
            *args,
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
        
        self.AppendItem(self.root_item, 'boobs')
        self.AppendItem(self.root_item, 'ass')
        self.AppendItem(self.root_item, 'tits')
        

