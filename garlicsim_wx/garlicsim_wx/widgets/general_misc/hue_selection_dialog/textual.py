import wx

def ratio_to_round_degrees(hue):
    return int(ratio * 360)

def degrees_to_ratio(degrees):
    return degrees / 360


class Textual(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 100))
        self.hue_selection_dialog = hue_selection_dialog
        self.hue = hue_selection_dialog.hue
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.hue_static_text = wx.StaticText(self, label='Hue:')
        #self.hue_static_text = wx.StaticText(self, label=''.join((chr(x) for x in range(256))))
        
        self.main_v_sizer.Add(self.hue_static_text, 0, wx.ALIGN_LEFT | wx.BOTTOM,
                              border=5)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 0)
        
        self.spin_ctrl = wx.SpinCtrl(self, min=0, max=359, size=(60, -1))
        
        self.h_sizer.Add(self.spin_ctrl, 0)
        
        #chr(248)
        self.degree_static_text = wx.StaticText(self, label=unichr(176))
        #self.degree_static_text.SetFont(
            #wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        #)
        
        self.h_sizer.Add(self.degree_static_text, 0)
        
        self.SetSizerAndFit(self.main_v_sizer)
                    
        
    def update(self):
        if self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue