# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `FreeContextMenu` class.

See its documentation for more details.
'''

import wx
from garlicsim_wx.general_misc import cute_menu


class FreeContextMenu(cute_menu.CuteMenu):
    '''
    Context menu shown in `StepProfilesList` when no step profile is selected.
    '''
    def __init__(self, step_profiles_list):
        super(FreeContextMenu, self).__init__()
        self.step_profiles_list = step_profiles_list
        self._build()
        
    def _build(self):
        '''Build the context menu.'''
        
        step_profiles_list = self.step_profiles_list
        
        self.new_step_profile_button = self.Append(
            -1,
            'Create step profile...',
            ' Create a new step profile'
        )
        self.Bind(wx.EVT_MENU,
                  step_profiles_list._on_new_step_profile_button,
                  source=self.new_step_profile_button)
        
    
    