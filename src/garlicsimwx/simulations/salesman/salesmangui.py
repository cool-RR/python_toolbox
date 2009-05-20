from salesman import *
import wx
import math



def initialize(gui_project):
    gui_project.text_ctrl=wx.TextCtrl(gui_project.state_showing_window,-1,style=wx.TE_MULTILINE)
    sizer=wx.BoxSizer(wx.VERTICAL)
    sizer.Add(gui_project.text_ctrl,1,wx.EXPAND)
    gui_project.state_showing_window.SetSizer(sizer)



def show_state(gui_project,state):

    mini = 1000000
    for i in range(NUM_OF_BIOMORPH):
        if mini > evalF(state.biomorph[i]):
            mini = evalF(state.biomorph[i])
    gui_project.text_ctrl.SetValue(str(mini))
    """
    p = []
    for i in range(10):
        p+= [evalF(state.biomorph[i])]
    p.sort()
    print p
    """
    pass
