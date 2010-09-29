import wx

from garlicsim.general_misc import address_tools

from . import colors


class ValueTextCtrl(wx.TextCtrl):
    
    def __init__(self, parent, value='', root=None):
        
        wx.TextCtrl.__init__(self, parent, value=value)
        
        self._original_background_color = self.GetBackgroundColour()
        
        self.root = root
        
        self.SetMinSize((10, -1))
        
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)
        
        self.Bind(wx.EVT_TEXT, self.on_text)
        
        self.error_mode = False
        
    
    def _check_validity_and_color(self):
        
        try:
            address_tools.resolve(str(self.GetValue()), root=self.root)
        except Exception:
            is_valid = False
        else:
            is_valid = True
            
        if is_valid:
            self.SetBackgroundColour(self._original_background_color)
        else: # not is_valid
            self.SetBackgroundColour(colors.get_error_background_color())
        self.Refresh()
        return is_valid
            
        
    def on_text(self, event):
        if self.error_mode:
            self._check_validity_and_color()
            
            
    def on_kill_focus(self, event):
        if self.FindFocus() != self:
            self.error_mode = not self._check_validity_and_color()