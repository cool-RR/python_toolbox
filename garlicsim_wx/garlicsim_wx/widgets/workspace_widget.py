#tododoc


import garlicsim_wx
from garlicsim_wx.general_misc.third_party import aui
from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import string_tools

class WorkspaceWidget(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, frame):
    
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.aui_manager = frame.aui_manager
        assert isinstance(self.aui_manager, aui.AuiManager)
        
        # I put these asserts mainly for better source assistance in Wing.
        # They may be removed.        

    @classmethod
    def get_uppercase_name(cls):
        return string_tools.camelcase_to_spacecase(cls.__name__).upper()
    
    def get_aui_pane_info(self):
        return self.aui_manager.GetPane(self)
        
    