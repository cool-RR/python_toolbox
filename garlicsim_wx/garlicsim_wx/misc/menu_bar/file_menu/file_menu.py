import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

class FileMenu(CuteMenu):
    def __init__(self, frame):
        super(FileMenu, self).__init__()
        self.frame = frame
        
        self.new_button = self.Append(
            -1, 
            '&New...\tCtrl+N',
            ' Create a new simulation'
        )
        frame.Bind(wx.EVT_MENU, frame.on_new, self.new_button)