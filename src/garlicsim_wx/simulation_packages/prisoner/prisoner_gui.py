# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

from prisoner import *
import wx.lib.agw.piectrl as piectrl
import wx
import math



def initialize(gui_project):
    color_dict={Angel:wx.NamedColor("White"), Asshole:wx.NamedColor("Black"), Smarty:wx.NamedColor("Blue")}
    gui_project.pie=piectrl.PieCtrl(gui_project.state_showing_window,-1,size=(300,300))
    gui_project.pie.GetLegend().SetLabelFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, True, 'Arial'))
    gui_project.pie.SetAngle(math.pi)

    gui_project.pie_part_dict={}
    for player_type in player_types:
        part=piectrl.PiePart()
        part.SetLabel(player_type.__name__)
        part.SetValue(1)
        part.SetColour(color_dict[player_type])
        gui_project.pie._series.append(part)
        gui_project.pie_part_dict[player_type]=part

    """
    sizer=wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(gui_project.pie,1,wx.EXPAND)
    gui_project.state_showing_window.SetSizer(sizer)
    sizer.Fit(gui_project.state_showing_window)
    """


def show_state(gui_project,state):
    for player_type in player_types:
        part = gui_project.pie_part_dict[player_type]
        value = how_many_players_of_certain_type(state.player_pool, player_type)
        part.SetValue(value)
    pass
