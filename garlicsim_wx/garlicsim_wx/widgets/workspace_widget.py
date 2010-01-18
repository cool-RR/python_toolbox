#tododoc

import wx.lib.agw.aui

from garlicsim.general_misc.third_party import abc

class WorkspaceWidget(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, gui_project):
        
        self.gui_project = gui_project
        self.frame = gui_project.frame
        
        self.frame.aui_manager.AddPane(
            self,
            wx.lib.agw.aui.AuiPaneInfo().Left().Caption(type(self).__name__)
        )
                             
        self.aui_manager.Update()

        
    