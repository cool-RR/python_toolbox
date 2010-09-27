import wx

from garlicsim.general_misc.third_party import inspect

from .star_arg import StarArg


class StarArgBox(wx.StaticBox):
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control,
                              label='Additional arguments')
        
        self.sizer = wx.StaticBoxSizer(self, wx.HORIZONTAL)
        
        self.step_function = step_function
        
        arg_spec = inspect.getargspec(step_function)
        
        star_arg_list = \
            argument_control.step_profile_dialog.step_functions_to_star_args[
                step_function
            ]
        
        
        self.star_args = []
        
        for star_arg_value in star_arg_list:
            star_arg = StarArg(argument_control, repr(star_arg_value))
            self.star_args.append(star_arg)
            self.sizer.Add(star_arg, 0)
            
    
        empty_star_arg = StarArg(argument_control, '', '')
        self.star_args.append(empty_star_arg)
        self.sizer.Add(empty_star_arg, 0)
        
        