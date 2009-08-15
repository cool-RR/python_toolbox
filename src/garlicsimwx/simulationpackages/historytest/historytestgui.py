import wx

def initialize(gui_project):
    gui_project.text_ctrl=wx.TextCtrl(gui_project.state_showing_window,-1,style=wx.TE_MULTILINE)
    sizer=wx.BoxSizer(wx.VERTICAL)
    sizer.Add(gui_project.text_ctrl,1,wx.EXPAND)
    gui_project.state_showing_window.SetSizer(sizer)



def show_state(gui_project,state):
    gui_project.text_ctrl.SetValue(str(state.number))

