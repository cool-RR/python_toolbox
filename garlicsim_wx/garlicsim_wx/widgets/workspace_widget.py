#tododoc


import garlicsim_wx
from garlicsim_wx.general_misc.third_party import aui
from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import string_tools

class WorkspaceWidget(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, frame, aui_pane_info=None):
    
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        # I put these asserts mainly for better source assistance in Wing.
        # They may be removed.
        
        class_name = self.__class__.__name__
        
        self.aui_pane_info = aui_pane_info or \
            aui.AuiPaneInfo().\
            Caption(string_tools.camelcase_to_spacecase(class_name).upper()).\
            CloseButton(False)
        
        frame.aui_manager.AddPane(
            self,
            self.aui_pane_info
        )
                             
        frame.aui_manager.Update()

        
    