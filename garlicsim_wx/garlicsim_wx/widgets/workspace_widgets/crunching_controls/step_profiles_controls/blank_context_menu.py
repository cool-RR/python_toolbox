import wx
from garlicsim_wx.general_misc import cute_menu

class BlankContextMenu(cute_menu.CuteMenu):
    # todo: rename? blank sounds like it's empty
    def __init__(self, step_profiles_list):
        super(BlankContextMenu, self).__init__()
        self.step_profiles_list = step_profiles_list
        self._build()
        
    def _build(self):
        
        step_profiles_list = self.step_profiles_list
        
        self.new_step_profile_button = self.Append(
            -1,
            'Create new step profile...',
            ' Create a new step profile'
        )
        self.Bind(wx.EVT_MENU,
                  step_profiles_list.on_new_step_profile_button,
                  source=self.new_step_profile_button)
    