import wx
from garlicsim_wx.widgets.general_misc import CuteDialog


class HueSelector(CuteDialog):
    
    def __init__(self, parent, lightness=1, saturation=1, id=-1,
                 title='Select hue', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE,
                 name=wx.DialogNameStr):

        
        CuteDialog.__init__(self, parent, id, title, pos, size, style, name)
        
        self.lightness = lightness
        self.saturation = saturation
        
        self.main_h_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.