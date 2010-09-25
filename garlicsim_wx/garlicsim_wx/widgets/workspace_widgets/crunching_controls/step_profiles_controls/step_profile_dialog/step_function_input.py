import wx

import garlicsim_wx


class StepFunctionInput(wx.ComboBox):
    def __init__(self, step_profile_dialog, value):
        self.step_profile_dialog = step_profile_dialog
        self.simpack_grokker = step_profile_dialog.simpack_grokker
        step_functions_list = [
            step_profile_dialog.step_function_to_address(step_function) for
            step_function in self.simpack_grokker.all_step_functions
        ]
        
        wx.ComboBox.__init__(self, step_profile_dialog, value=value,
                             choices=step_functions_list, size=(200, -1))
        
        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_box)
        
        self.try_taking_step_function()

        
    def try_taking_step_function(self):
        text = self.GetValue()
        pass        
        
    
    def on_text(self, event):
        self.try_taking_step_function()
    
        
    def on_combo_box(self, event):
        self.try_taking_step_function()
        
        