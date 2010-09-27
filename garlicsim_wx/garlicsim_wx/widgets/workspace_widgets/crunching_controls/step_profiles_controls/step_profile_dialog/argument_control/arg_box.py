import wx

from garlicsim.general_misc.third_party import inspect

from .arg import Arg


class ArgBox(wx.StaticBox):
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control,
                              label='Arguments')
        
        self.sizer = wx.StaticBoxSizer(self, wx.HORIZONTAL)
        
        self.step_function = step_function
        
        arg_spec = inspect.getargspec(step_function)
        
        arg_dict = self.step_profile_dialog.step_functions_to_argument_dicts[
            step_function
        ]
        
        self.args = []
        
        for i, arg_name in list(enumerate(arg_spec.args))[1:]:
            value = repr(arg_dict[arg_name])
            if not value and (arg_name in arg_spec.defaults):
                value = arg_dict[arg_name] = repr(arg_spec.defaults[i])
            arg = Arg(argument_control, arg_name, value)
            self.args.append(arg)
            self.sizer.Add(arg, 0)
            