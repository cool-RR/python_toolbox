# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the NodeMenu class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu


class ForkByCrunchingUsingMenu(CuteMenu):
    def __init__(self, frame):
        super(ForkByCrunchingUsingMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        

        self.AppendSeparator()
        
        
        self.new_step_profile_button = self.Append(
            -1,
            '&New step profile...',
            ' Create a new step profile'
        )
        frame.Bind(wx.EVT_BUTTON, self.on_new_step_profile_button,
                   self.new_step_profile_button)
        
        
    def on_new_step_profile_button(self, event):
        raise NotImplementedError#tododoc
    
        
    def _recalculate(self):
        gui_project = self.frame.gui_project
        if not gui_project:
            return
        step_profiles = gui_project.step_profiles
        
        # Getting the existing menu items, while slicing out the separator and
        # "New step profile..." button:
        items = list(self.GetMenuItems())[:-2]
        items_iterator = iter(items)
        
        for i, step_profile in enumerate(step_profiles):
            current_item = items_iterator.next()
            if current_item.step_profile == step_profile:
                continue
            step_profile_text = step_profile.__repr__(
                short_form=True,
                root=gui_project.simpack,
                namespace=gui_project.namespace
            )
            new_item = self.Insert(
                i,
                -1,
                step_profile_text,
                'Fork by crunching using %s' % step_profile_text
            )
                
            
            
        
        
        
        
    