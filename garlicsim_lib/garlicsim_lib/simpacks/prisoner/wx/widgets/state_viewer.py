# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the StateViewer class.

See its documentation for more information.
'''

import math

import wx
import wx.lib.agw.piectrl as piectrl

import garlicsim_wx

from ... import state as prisoner


class StateViewer(wx.Panel, garlicsim_wx.widgets.WorkspaceWidget):
    '''Widget for viewing a `prisoner` state.'''
    def __init__(self, frame):
        wx.Panel.__init__(self, frame)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.pie_ctrl = piectrl.PieCtrl(self, style=wx.NO_BORDER)
        
        self.sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v.Add(self.sizer_h, 1, wx.EXPAND)
        self.sizer_h.Add(self.pie_ctrl, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer_v)
        self.sizer_v.Layout()
        
        color_dict = {
            prisoner.Angel: wx.NamedColor("White"),
            prisoner.Asshole: wx.NamedColor("Black"),
            prisoner.Smarty: wx.NamedColor("Blue")
        }
        
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, True, 'Arial')
        self.pie_ctrl.GetLegend().SetLabelFont(font)
        self.pie_ctrl.SetAngle(math.pi)
    
        self.pie_part_dict = {}
        for player_type in prisoner.player_types:
            part = piectrl.PiePart()
            part.SetLabel(player_type.__name__)
            part.SetValue(1)
            part.SetColour(color_dict[player_type])
            self.pie_ctrl._series.append(part)
            self.pie_part_dict[player_type] = part
            
        self.gui_project.active_node_changed_or_modified_emitter.add_output(
            lambda: self.show_state(self.gui_project.get_active_state())
        )
            
    def show_state(self, state):
        '''Show a state onscreen.'''
        if state is None:
            return
        for player_type in prisoner.player_types:
            part = self.pie_part_dict[player_type]
            value = prisoner.how_many_players_of_certain_type(
                state.player_pool,
                player_type
            )
            part.SetValue(value)
        self.Refresh()
