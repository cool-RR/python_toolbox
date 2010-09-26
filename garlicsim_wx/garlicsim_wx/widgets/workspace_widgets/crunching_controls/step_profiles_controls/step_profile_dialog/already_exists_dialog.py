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
            label='The step profile `%s` already exists.'
        )
        
        self.main_v_sizer.Add(self.static_text, 0, wx.EXPAND)
        

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.button_sizer, 0, wx.EXPAND)
        
        
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
        
        
        
    def on_take_me_to_it_button(self, event):
        self.EndModal(wx.ID_OK)
        self.frame.crunching_controls.show()
        step_profiles_list = self.frame.crunching_controls.\
                             step_profiles_controls.step_profiles_list
        step_profiles_list.SetFocus()
        item = step_profiles_list.step_profiles_to_items[self.step_profile]
        step_profiles_list.SelectItem(item)
    
    
    def on_keep_editing_button(self, event):
        self.EndModal(wx.ID_CANCEL)
        