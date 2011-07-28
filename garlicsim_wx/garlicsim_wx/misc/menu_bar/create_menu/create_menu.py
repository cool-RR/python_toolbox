# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CreateMenu` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu


class CreateMenu(CuteMenu):
    '''Menu for creating new objects.'''
    def __init__(self, frame):
        super(CreateMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
        self.create_state_button = self.Append(
            -1, 
            'Create &State...',
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
            'Create Step &Profile...',
            ' Create a new step profile, which can modify the world rules '
            'under which the simulation crunches'
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: frame.crunching_controls.step_profiles_controls.\
                          show_step_profile_editing_dialog(),
            self.create_step_profile_button
        )
        
        
    def _recalculate(self):
        self.enable_in_menu_bar(
            self.frame.gui_project is not None
        )