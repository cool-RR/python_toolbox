import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog

from .static_function_text import StaticFunctionText
from .step_function_input import StepFunctionInput
from .argument_list import ArgumentList


class StepProfileDialog(CuteDialog):
    # tododoc: this class will be responsible for checking if the new step
    # profile is already present in the step_profiles set.
    
    def __init__(self, step_profiles_controls, step_profile=None):
        
        self.step_profiles_controls = step_profiles_controls
        
        CuteDialog.__init__(self, step_profiles_controls.frame,
                            title='Create a new step profile')
        
        self.original_step_profile = step_profile

        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        self.static_function_text = StaticFunctionText(self)
        
        self.main_v_sizer.Add(
            self.static_function_text,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,
            border=10
        )

        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(
            self.h_sizer,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,            
            border=10
        )
        
        
        self.step_function_input = StepFunctionInput(self)
        
        self.h_sizer.Add(
            self.step_function_input,
            0,
            wx.ALIGN_TOP | wx.ALL,            
            border=5
        )
        
        
        self.argument_list = ArgumentList(self)
        
        self.h_sizer.Add(
            self.argument_list,
            1,
            wx.EXPAND | wx.ALL,
            border=5
        )
        
        
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        
        self.main_v_sizer.Add(
            self.dialog_button_sizer,
            0,
            wx.ALIGN_CENTER | wx.ALL,
            border=10
        )
        
        self.ok_button = wx.Button(self, wx.ID_OK, 'Create step profile')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        self.dialog_button_sizer.Realize()
    
        
        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
        
    
    def on_ok(self, event):
        pass
    
    
    def on_cancel(self, event):
        pass
                         
        