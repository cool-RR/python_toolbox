import wx

import garlicsim_wx


class StateViewer(wx.Panel,
                  garlicsim_wx.widgets.WorkspaceWidget):
    # Here you create a widget that will display your state graphically on the
    # screen.
    
    def __init__(self, frame):
            
        # We need to call the __init__ of both our base classes:
        wx.Panel.__init__(self, frame,
                                        style=wx.SUNKEN_BORDER)        
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM) # Solves Windows flicker
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        
        # ...
        

        # This next bit will cause the widget to get updated every time the
        # active state in the GUI is changed:
        self.gui_project.active_node_changed_emitter.add_output(
            lambda: self.set_state(self.gui_project.get_active_state())
        )


    def set_state(self, state):
        # Here you set the state to be displayed.
        self.state = state
        self.Refresh()
        
        
    def on_paint(self, event):
        # This is your EVT_PAINT handler, which draws the state on the widget.
        
        event.Skip()
        
        dc = wx.PaintDC(self)
        
        # ...
        
        dc.Destroy()
        
        
    def on_size(self, event):
        # An EVT_SIZE handler. Just some wxPython thing that I think you're
        # supposed to do.
        self.Refresh()

