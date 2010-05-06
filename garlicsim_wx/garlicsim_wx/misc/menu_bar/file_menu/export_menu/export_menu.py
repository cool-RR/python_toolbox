import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

class ExportMenu(CuteMenu):
    def __init__(self, frame):
        super(ExportMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
        
        self.video_button = self.Append(
            -1,
            '&Video',
            ' Export a video sequence showing playback of the simulation'
        )
        self.video_button.Enable(False)
        
        
        self.image_button = self.Append(
            -1,
            '&Image',
            ' Export an image showing a single state in the simulation'
        )
        self.image_button.Enable(False)
                
