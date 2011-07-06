# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `AlreadyExistsDialog` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog

import garlicsim_wx


class AlreadyExistsDialog(CuteDialog):
    '''
    Dialog alerting that the step profile you tried to create already exists.
    
    The user may either go to the existing step profile, or keep editing this
    one.
    '''
    def __init__(self, step_profile_dialog, step_profile, and_fork=False):
        '''
        Construct the `AlreadyExistsDialog`.
        
        Set `and_fork=True` if you intend to fork right after getting the step
        profile, though note it will only affect the labels; the actual forking
        is not done here.
        '''
        self.step_profile_dialog = step_profile_dialog
        self.frame = step_profile_dialog.frame
        self.step_profile = step_profile
        self.and_fork = and_fork
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        CuteDialog.__init__(self, step_profile_dialog,
                            title='Step profile already exists')

        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
                
        
        self.static_text = wx.StaticText(
            self,
            label='The step profile `%s` already exists.' % \
                step_profile.__repr__(
                    short_form=True,
                    root=self.frame.gui_project.simpack,
                    namespace=self.frame.gui_project.namespace
                )
        )
        
        self.main_v_sizer.Add(self.static_text, 0, wx.EXPAND | wx.ALL,
                              border=10)
        

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.button_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        take_me_to_it_label = '&Take me to it' if not and_fork else \
                              '&Take me to it and fork with it'
        self.take_me_to_it_button = wx.Button(self, label=take_me_to_it_label)
        
        # Allowing keyboard-navigation and Esc on Ubuntu:
        self.take_me_to_it_button.SetFocus()
        
        self.button_sizer.Add(self.take_me_to_it_button, 0, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.keep_editing_button = wx.Button(self, label='&Keep editing')
        
        
        
        self.SetEscapeId(self.keep_editing_button.Id)
        
        self.button_sizer.Add(self.keep_editing_button, 0, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.take_me_to_it_button.SetDefault()
        
        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
        self.bind_event_handlers(AlreadyExistsDialog)
        
        
    def _on_take_me_to_it_button(self, event):
        self.EndModal(wx.ID_OK)
        step_profiles_list = self.frame.crunching_controls.\
                             step_profiles_controls.step_profiles_list
        step_profiles_list.select_step_profile(self.step_profile)
        self.frame.crunching_controls.show()

        # Hacky, since `wx.CallAfter` doesn't work for this:
        wx.CallLater(200, step_profiles_list.real_set_focus)
        
    
    def _on_keep_editing_button(self, event):
        self.EndModal(wx.ID_CANCEL)
        
    