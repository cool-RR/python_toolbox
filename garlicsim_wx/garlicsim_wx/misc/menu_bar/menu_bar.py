import wx

from file_menu import FileMenu

class MenuBar(wx.MenuBar):
    def __init__(self, frame):
        super(MenuBar, self).__init__()
        self.frame = frame
        
        self.file_menu = FileMenu(frame)
        self.Append(self.file_menu, '&File')