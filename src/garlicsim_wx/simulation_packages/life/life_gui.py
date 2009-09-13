import garlicsim.data_structures
import random
import warnings
import functools

import wx
import custom_widgets
def initialize(gui_project):
    gui_project.mysizer=wx.BoxSizer(wx.VERTICAL)
    board_widget=gui_project.board_widget=custom_widgets.BoardWidget(gui_project.state_showing_window,-1,gui_project)
    gui_project.mysizer.Add(board_widget,1,wx.EXPAND)
    gui_project.state_showing_window.SetSizer(gui_project.mysizer)
    gui_project.mysizer.Fit(gui_project.state_showing_window)

def show_state(gui_project,state):
    gui_project.board_widget.set_board(state.board)

################

class InitialDialog(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, title="Creating a root state")

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        self.x_title=x_title=wx.StaticText(self,-1,"Width: ")
        self.x_textctrl=x_textctrl=wx.TextCtrl(self, -1, "50")
        self.y_title=y_title=wx.StaticText(self,-1,"Height: ")
        self.y_textctrl=y_textctrl=wx.TextCtrl(self, -1, "30")
        hbox1.Add(x_title,0,wx.ALIGN_CENTER |wx.EXPAND | wx.ALL,5)
        hbox1.Add(x_textctrl,0,wx.EXPAND | wx.ALIGN_CENTER |wx.RIGHT,40)
        hbox1.Add(y_title,0,wx.EXPAND | wx.ALIGN_CENTER |wx.RIGHT,10)
        hbox1.Add(y_textctrl,0,wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT,5)

        hbox2=wx.BoxSizer(wx.HORIZONTAL)
        self.empty=empty=wx.RadioButton(self, -1, 'All empty', style=wx.RB_GROUP)
        self.full=full=wx.RadioButton(self, -1, 'All full')
        self.random=random=wx.RadioButton(self, -1, 'Random')
        random.SetValue(True)
        hbox2.Add(empty,0,wx.ALIGN_CENTER | wx.ALL,5)
        hbox2.Add(full,0,wx.ALIGN_CENTER | wx.ALL,5)
        hbox2.Add(random,0,wx.ALIGN_CENTER | wx.ALL,5)


        vbox = wx.BoxSizer(wx.VERTICAL)


        last_hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok=wx.Button(self, -1, 'Ok', size=(70, 30))
        ok.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=ok.GetId())
        cancel=wx.Button(self, -1, 'Cancel', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.on_cancel, id=cancel.GetId())
        last_hbox.Add(ok, 0)
        last_hbox.Add(cancel, 0, wx.LEFT, 5)

        vbox.Add(hbox1,0,wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(hbox2,0,wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(last_hbox, 1, wx.ALIGN_CENTER |  wx.BOTTOM, 10)

        self.SetSizer(vbox)
        vbox.Fit(self)
        ok.SetFocus()

    def on_ok(self,e=None):

        def complain(message):
            dialog=wx.MessageDialog(self,message,"Error",wx.ICON_ERROR | wx.OK)
            dialog.ShowModal(); dialog.Destroy()

        self.info={}

        try:
            self.info["width"]=int(self.x_textctrl.GetValue())
        except ValueError:
            complain("Bad width!")
            return

        try:
            self.info["height"]=int(self.y_textctrl.GetValue())
        except ValueError:
            complain("Bad height!")
            return

        self.info["fill"]="full" if self.full.GetValue() else "empty" if self.empty.GetValue() else "random"


        self.EndModal(wx.ID_OK)

    def on_cancel(self,e=None):
        self.EndModal(wx.ID_CANCEL)



def make_initial_dialog(gui_project):
    initial_dialog=InitialDialog(gui_project.main_window, -1)
    if initial_dialog.ShowModal()==wx.ID_OK:
        (width,height,fill)=(initial_dialog.info["width"],
                             initial_dialog.info["height"],
                             initial_dialog.info["fill"])
        gui_project.make_plain_root(width,height,fill)
    initial_dialog.Destroy()