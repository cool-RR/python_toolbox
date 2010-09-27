import wx

from garlicsim.general_misc.third_party import inspect

from .arg_box import ArgBox
from .star_arg_box import StarArgBox
from .star_kwarg_box import StarKwargBox


class ArgumentControl(wx.Panel):
    def __init__(self, step_profile_dialog, step_function=None):
        self.step_profile_dialog = step_profile_dialog
        self.gui_project = step_profile_dialog.gui_project
        
        wx.Panel.__init__(self, step_profile_dialog)
        
        self.box_size = wx.Size(200, -1)
        
        self.step_function = None
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.build_for_step_function(step_function)
        

        
    def build_for_step_function(self, step_function):
        if self.step_function == step_function:
            return
        self.DestroyChildren()
        
        arg_spec = inspect.getargspec(step_function)
        
        step_profile_dialog = self.step_profile_dialog
        
        arg_dict = step_profile_dialog.step_functions_to_argument_dicts[
            step_function
        ]
        
        star_arg_list = step_profile_dialog.step_functions_to_star_args[
            step_function
        ]
        
        star_kwarg_dict = step_profile_dialog.step_functions_to_star_kwargs[
            step_function
        ]
        
        
        if arg_spec.args:
            self.arg_box = ArgBox(self, step_function)
            self.main_h_sizer.Add(self.arg_box.sizer, 0, wx.ALL, border=10)
        else:
            self.arg_box = None
            self.main_h_sizer.Add(self.box_size, 0, wx.ALL, border=10)
            
        
        if arg_spec.varargs:
            self.star_arg_box = StarArgBox(self, step_function)
            self.main_h_sizer.Add(self.star_arg_box.sizer, 0, wx.ALL,
                                  border=10)
        else:
            self.star_arg_box = None
            self.main_h_sizer.Add(self.box_size, 0, wx.ALL, border=10)
                
            
        if arg_spec.keywords:
            self.star_kwarg_box = StarKwargBox(self, step_function)
            self.main_h_sizer.Add(self.star_kwarg_box.sizer, 0, wx.ALL,
                                  border=10)
        else:
            self.star_kwarg_box = None
            self.main_h_sizer.Add(self.box_size, 0, wx.ALL, border=10)
            
        
        self.main_h_sizer.Fit(self)