# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ForkByCrunchingUsingMenu` class.

See its documentation for more details.
'''

from itertools import izip

from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim.general_misc.sleek_refs import CuteSleekValueDict
import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu


class ForkByCrunchingUsingMenu(CuteMenu):
    def __init__(self, frame):
        super(ForkByCrunchingUsingMenu, self).__init__()
        self.frame = frame
        self.item_ids_to_step_profiles = CuteSleekValueDict(lambda: None)
        self._build()
    
    def _build(self):
        
        frame = self.frame
        

        self.AppendSeparator()
        
        
        self.new_step_profile_button = self.Append(
            -1,
            '&New step profile...',
            ' Create a new step profile and fork with it'
        )
        frame.Bind(wx.EVT_MENU, self._on_new_step_profile_button,
                   self.new_step_profile_button)
        
        
    def _on_new_step_profile_button(self, event):
        self.frame.crunching_controls.show()
        self.frame.crunching_controls.step_profiles_controls.\
            show_step_profile_editing_dialog(and_fork=True)
        

    def _get_step_profile_items(self):
        '''Get the menu items which correspond to step profiles.'''
        # Getting the existing menu items, while slicing out the separator and
        # "New step profile..." button:
        return list(self.GetMenuItems())[:-2]
    
        
    def _recalculate(self):
        gui_project = self.frame.gui_project
        if not gui_project:
            return
        step_profiles = gui_project.step_profiles
            
        items = self._get_step_profile_items()
        
        def find_item_of_step_profile(step_profile):
            '''Find the menu item corresponding to `step_profile`.'''
            matching_items = \
                [item for item in items if 
                self.item_ids_to_step_profiles[item.Id] == step_profile]
            assert len(matching_items) in [0, 1]
            if matching_items:
                (matching_item,) = matching_items
                return matching_item
            else:
                return None
        
        step_profiles_to_items = OrderedDict(
            ((step_profile, find_item_of_step_profile(step_profile))
             for step_profile in step_profiles)
        )
        
        needed_items = filter(None, step_profiles_to_items.values())
        unneeded_items = [item for item in items if (item not in needed_items)]
        
        for unneeded_item in unneeded_items:
            self.frame.Unbind(wx.EVT_MENU, unneeded_item)
        
        for item in items:
            self.RemoveItem(item)
            
        itemless_step_profiles = [
            step_profile for step_profile in step_profiles if
            (step_profiles_to_items[step_profile] is None)
        ]
        
        for step_profile in itemless_step_profiles:
            step_profile_text = step_profile.__repr__(
                short_form=True,
                root=gui_project.simpack,
                namespace=gui_project.namespace
            )
            new_item = wx.MenuItem(
                self,
                -1,
                step_profile_text,
                'Fork by crunching using %s' % step_profile_text
            )
            self.item_ids_to_step_profiles[new_item.Id] = step_profile
            step_profiles_to_items[step_profile] = new_item
            self.frame.Bind(
                wx.EVT_MENU,
                lambda event:
                    gui_project.fork_by_crunching(step_profile=step_profile),
                new_item
            )
            
        for i, item in enumerate(step_profiles_to_items.itervalues()):
            self.InsertItem(i, item)
            
        
        updated_items = self._get_step_profile_items()
        for item, step_profile in izip(updated_items, step_profiles):
            assert self.item_ids_to_step_profiles[item.Id] == step_profile
            
        
                
            