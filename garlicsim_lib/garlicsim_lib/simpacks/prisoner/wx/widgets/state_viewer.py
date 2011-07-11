1# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StateViewer` class.

See its documentation for more information.
'''

import math

import wx
import wx.lib.agw.piectrl as piectrl

from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

import garlicsim_wx

from garlicsim_lib.simpacks import prisoner


class StateViewer(CutePanel, garlicsim_wx.widgets.WorkspaceWidget):
    '''Widget for viewing a `prisoner` state.'''
    def __init__(self, frame):
        CutePanel.__init__(self, frame)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.pie_ctrl = piectrl.PieCtrl(self, style=wx.NO_BORDER)
        
        self.sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v.Add(self.sizer_h, 1, wx.EXPAND)
        self.sizer_h.Add(self.pie_ctrl, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer_v)
        self.sizer_v.Layout()
        
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, True, 'Arial')
        self.pie_ctrl.GetLegend().SetLabelFont(font)
        self.pie_ctrl.SetAngle(math.pi)
    
        self.pie_part_dict = {}
        for player_type in prisoner.players.player_types_list:
            part = piectrl.PiePart()
            part.SetLabel(player_type.__name__)
            part.SetValue(1)
            part.SetColour(player_type.wx_color)
            self.pie_ctrl._series.append(part)
            self.pie_part_dict[player_type] = part
            
        self.gui_project.active_node_changed_or_modified_emitter.add_output(
            lambda: self.show_state(self.gui_project.get_active_state())
        )
            
    def show_state(self, state):
        '''Show a state onscreen.'''
        if state is None:
            return
        for player_type in prisoner.players.player_types_list:
            part = self.pie_part_dict[player_type]
            value = state.get_n_players_of_given_type(player_type)
            part.SetValue(value)
        self.Refresh()
