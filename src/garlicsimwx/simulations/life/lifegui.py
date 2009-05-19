import garlicsim.state
import random
import warnings

import wx
import customwidgets
def initialize(gui_project):
    gui_project.mysizer=wx.BoxSizer(wx.VERTICAL)
    board_widget=gui_project.board_widget=customwidgets.BoardWidget(gui_project.state_showing_window,-1,gui_project)
    gui_project.mysizer.Add(board_widget,1,wx.EXPAND)
    gui_project.state_showing_window.SetSizer(gui_project.mysizer)
    gui_project.mysizer.Fit(gui_project.state_showing_window)

def show_state(gui_project,state):
    gui_project.board_widget.set_board(state.board)