# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
garlicsim_wx interface for the queue simpack.
'''

import wx

import garlicsim.data_structures
import custom_widgets

def initialize(gui_project):
    '''Initialize the gui.'''
    gui_project.mysizer = wx.BoxSizer(wx.VERTICAL)
    state_shower = gui_project.state_shower = \
        custom_widgets.StateShower(gui_project.state_showing_window, -1,
                                   gui_project)
    gui_project.mysizer.Add(state_shower, 1, wx.EXPAND)
    gui_project.state_showing_window.SetSizer(gui_project.mysizer)
    gui_project.mysizer.Fit(gui_project.state_showing_window)

def show_state(gui_project, state):
    '''Show the given state onscreen.'''
    gui_project.state_shower.load_state(state)
