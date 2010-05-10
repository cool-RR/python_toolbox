import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu


class CreateMenu(CuteMenu):
    def __init__(self, frame):
        super(CreateMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
        self.create_state_button = self.Append(
            -1, 
            'Create &state...',
            ' Create a new state, which will become a root node in the tree'
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: frame.gui_project.make_state_creation_dialog(),
            self.create_state_button
        )
        
    
        self.AppendSeparator()
        
        
        self.create_step_profile_button = self.Append(
            -1, 
            'Create step &profile...',
            ''' Create a new step profile, which can modify the world rules \
under which the simulation crunches'''
        )
        self.create_step_profile_button.Enable(False)
        
        