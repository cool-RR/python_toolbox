import wx
from garlicsim_wx.general_misc import cute_menu

class StepProfileContextMenu(cute_menu.CuteMenu):
    def __init__(self, step_profiles_list):
        super(StepProfileContextMenu, self).__init__()
        self.step_profiles_list = step_profiles_list
        self._build()
        
    def _build(self):
        
        step_profiles_list = self.step_profiles_list
        
        self.fork_by_crunching_button = self.Append(
            -1,
            'Fork by &crunching...',
            ' Fork the simulation by crunching from the active node using this step profile'
        )
        self.Bind(wx.EVT_MENU,
                  step_profiles_list.on_fork_by_crunching_button,
                  source=self.fork_by_crunching_button)
        
        
        self.AppendSeparator()
        
        
        self.select_tree_members_button = self.Append(
            -1,
            'Select tree &members',
            ' Select all the nodes and ends that have this step profile'
        )
        self.Bind(wx.EVT_MENU,
                  step_profiles_list.on_select_tree_members_button,
                  source=self.select_tree_members_button)
        
        
        self.AppendSeparator()
        
        
        self.change_color_button = self.Append(
            -1,
            'Change co&lor...',
            ' Change the color of this step profile'
        )
        self.Bind(wx.EVT_MENU,
                  step_profiles_list.on_change_color_button,
                  source=self.change_color_button)
        
        
        self.duplicate_and_edit_button = self.Append(
            -1,
            '&Duplicate and edit...',
            ' Duplicate this step profile and edit the newly-created step profile'
        )
        self.Bind(wx.EVT_MENU,
                  step_profiles_list.on_duplicate_and_edit_button,
                  source=self.duplicate_and_edit_button)
        
        
        self.delete_button = self.Append(
            -1,
            'D&elete...\tDel', # tododoc: Can Del work?
            ' Delete this step profile'
        )
        self.Bind(wx.EVT_MENU,
                  step_profiles_list.on_delete_button,
                  source=self.delete_button)
        
        
    