import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

class BlockMenu(CuteMenu):
    def __init__(self, frame):
        super(BlockMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
       
        self.split_button = self.Append(
            -1,
            '&Split active block...',
            " Split the active block into two separate blocks"
        )
        self.split_button.Enable(False)
        
        
        self.scatter_button = self.Append( # todo: rename
            -1,
            'S&catter active block...',
            ' Scatter the active block, leaving all its nodes blockless'
        )
        self.scatter_button.Enable(False)
        
        