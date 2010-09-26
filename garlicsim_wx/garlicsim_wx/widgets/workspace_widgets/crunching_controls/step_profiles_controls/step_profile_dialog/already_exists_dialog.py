import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog

import garlicsim_wx


class AlreadyExistsDialog(CuteDialog):
    def __init__(self, step_profile_dialog, step_profile):
        self.step_profile_dialog = step_profile_dialog
        self.frame = step_profile_dialog.frame
        self.step_profile = step_profile
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        CuteDialog.__init__(self, step_profile_dialog,
                            title='Step profile already exists')

        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
                
        
        self.static_text = wx.StaticText(
            self,
            label='The step profile `%s` already exists.' % \
                step_profile.__repr__(
                    short_form=True,
                    root=self.frame.gui_project.simpack
                )
        )
        
        self.main_v_sizer.Add(self.static_text, 0, wx.EXPAND | wx.ALL,
                              border=10)
        

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.button_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        
        self.take_me_to_it_button = wx.Button(self, label='Take me to it')
        
        self.button_sizer.Add(self.take_me_to_it_button, 0, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.keep_editing_button = wx.Button(self, label='Keep editing')
        
        self.button_sizer.Add(self.keep_editing_button, 0, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.Bind(wx.EVT_BUTTON, self.on_take_me_to_it_button,
                  source=self.take_me_to_it_button)
        self.Bind(wx.EVT_BUTTON, self.on_keep_editing_button,
                  source=self.keep_editing_button)
        
        self.take_me_to_it_button.SetDefault()
        
        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
        
        
        
    def on_take_me_to_it_button(self, event):
        # tododoc: test that it really puts the focus there. maybe callafter?
        wx.CallAfter(self._put_focus_on_step_profile, self.frame,
                     self.step_profile)
        self.EndModal(wx.ID_OK)
        
    
    
    def on_keep_editing_button(self, event):
        self.EndModal(wx.ID_CANCEL)
        
    
    @staticmethod
    def _put_focus_on_step_profile(frame, step_profile):
        step_profiles_list = \
            frame.crunching_controls.step_profiles_controls.step_profiles_list
        step_profiles_list.SetFocus()
        item = step_profiles_list.step_profiles_to_items[step_profile]
        step_profiles_list.SelectItem(item)
        frame.crunching_controls.show()