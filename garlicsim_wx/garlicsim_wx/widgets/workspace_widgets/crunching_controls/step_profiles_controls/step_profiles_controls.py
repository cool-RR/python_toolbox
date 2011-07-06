# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StepProfilesControls` class.

See its documentation for more details.
'''

import pkg_resources
import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_error_dialog import CuteErrorDialog
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

import garlicsim
import garlicsim_wx

from .step_profiles_list import StepProfilesList
from .step_profile_dialog import StepProfileDialog

from . import images as __images_package
images_package = __images_package.__name__

    
class StepProfilesControls(CutePanel):
    '''Widget for manipulating the step profiles used in the gui project.'''
    
    def __init__(self, parent, frame, *args, **kwargs):
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.set_good_background_color()
        
        self.SetToolTipString('Add, remove or organize step profiles.')

        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_text = wx.StaticText(self, -1, 'Step profiles:')
        
        self.main_v_sizer.Add(self.title_text, 0, wx.ALL, 10)
        
        self.step_profiles_list = StepProfilesList(self, frame)
        
        self.main_v_sizer.Add(self.step_profiles_list, 1,
                              wx.EXPAND | wx.BOTTOM, 8)
        
        self.button_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.button_h_sizer, 0, wx.ALIGN_RIGHT)
        
        new_image = wx_tools.bitmap_tools.bitmap_from_pkg_resources(
            images_package,
            'new.png'
        )
        self.new_button = wx.BitmapButton(self, -1, new_image)
        self.new_button.SetToolTipString('Create a new step profile.')
        
        self.button_h_sizer.Add(self.new_button, 0, wx.RIGHT, 8)
        
        delete_image = wx_tools.bitmap_tools.bitmap_from_pkg_resources(
            images_package,
            'trash.png'
        )
        self.delete_button = wx.BitmapButton(self, -1, delete_image)
        self.delete_button.SetToolTipString(
            'Delete the selected step profile.'
        )
        self.delete_button.Disable()
        
        self.button_h_sizer.Add(self.delete_button, 0, wx.RIGHT, 8)
        
        self.SetSizer(self.main_v_sizer)
        
        self.bind_event_handlers(StepProfilesControls)

        
    def _recalculate(self):
        if self.step_profiles_list.get_selected_step_profile():
            self.delete_button.Enable()
        else: # self.step_profiles_list.get_selected_step_profile() is None
            self.delete_button.Disable()
            
    
    def show_step_profile_editing_dialog(self, step_profile=None,
                                         and_fork=False):
        '''
        Show a dialog for creating a new step profile.
        
        `step_profile` is the step profile that will be used as a template; use
        `None` to start from scratch.
                
        Set `and_fork=True` to fork with the new (or identical existing) step
        profile after the dialog is done.
        '''
        
        # todo: It's a bitch that there's logic here for handling what happens
        # after the dialog is finished. Because there's related logic in the
        # dialog itself. Ideally the logic should be in one of those places
        # only, not spread between them.
        
        step_profile_dialog = StepProfileDialog(self, step_profile,
                                                and_fork=and_fork)
        
        try:
            if step_profile_dialog.ShowModal() == wx.ID_OK:
                new_step_profile = step_profile_dialog.step_profile
                new_hue = step_profile_dialog.hue
            else:
                new_step_profile = new_hue = None
        finally:
            step_profile_dialog.Destroy()
            
        if new_step_profile:
            assert new_step_profile not in self.gui_project.step_profiles
            self.gui_project.step_profiles_to_hues[new_step_profile] = new_hue
            self.gui_project.step_profiles.add(new_step_profile)
            self.step_profiles_list.select_step_profile(new_step_profile)
            
            
        if not and_fork:
            self.step_profiles_list.real_set_focus()
            
        if and_fork and step_profile_dialog.step_profile:
            self.frame.gui_project.fork_by_crunching(
                step_profile_dialog.step_profile
            )
            
            
    def try_delete_step_profile(self, step_profile):
        '''
        Try to delete `step_profile`, raising dialog if it's used in the tree.
        '''
        # todo: in the future, make this dialog offer to delete the nodes with
        # the step profile.
        if step_profile is None:
            return
        tree_step_profiles = self.gui_project.project.tree.get_step_profiles()
        if step_profile in tree_step_profiles:
            CuteErrorDialog.create_and_show_modal(
                self,
                "The step profile `%s` is currently used in the tree; it may "
                "not be deleted." % step_profile.__repr__(
                    short_form=True,
                    root=self.gui_project.simpack,
                    namespace=self.gui_project.namespace
                )
            )
            return
        else:
            self.gui_project.step_profiles.remove(step_profile)
            
            
    def _on_new_button(self, event):
        self.show_step_profile_editing_dialog(step_profile=None)
    
    
    def _on_delete_button(self, event):
        self.try_delete_step_profile(
            self.step_profiles_list.get_selected_step_profile()
        )