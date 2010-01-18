#tododoc

import wx.lib.agw.aui

from garlicsim.general_misc.third_party import abc

class WorkspaceWidget(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, frame):
        
        self.frame = frame
        
        frame.aui_manager.AddPane(
            self,
            wx.lib.agw.aui.AuiPaneInfo().Left().Caption(type(self).__name__)
        )
                             
        frame.aui_manager.Update()

        
    