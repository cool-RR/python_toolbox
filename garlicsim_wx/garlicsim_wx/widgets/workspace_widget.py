#tododoc

from garlicsim_wx.general_misc.third_party import aui
from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import string_tools

class WorkspaceWidget(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, frame):
        
        self.frame = frame
        
        self.gui_project = frame.gui_project
        
        class_name = self.__class__.__name__
        
        self.aui_pane_info = \
            aui.AuiPaneInfo().\
            Caption(string_tools.camelcase_to_spacecase(class_name).upper()).\
            Center().CloseButton(False)
        
        frame.aui_manager.AddPane(
            self,
            self.aui_pane_info
        )
                             
        frame.aui_manager.Update()

        
    