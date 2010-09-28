import wx

from garlicsim.general_misc.third_party import inspect

from .star_arg import StarArg
from .star_adder import StarAdder, EVT_STAR_ADDER_PRESSED


class StarArgBox(wx.StaticBox):
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control,
                              label='Additional arguments')
        
        self.SetMinSize(argument_control.box_size)
        self.SetMaxSize(argument_control.box_size)
        
        self.sizer = wx.StaticBoxSizer(self, wx.VERTICAL)
        
        self.sizer.SetMinSize(argument_control.box_size)
        
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
            self.sizer.Add(star_arg, 0, wx.EXPAND | wx.ALL, border=5)
            
        self.star_adder = StarAdder(self)
        self.sizer.Add(self.star_adder, 0, wx.EXPAND | wx.ALL, border=5)
        
        
        
    def on_star_adder_pressed(self, event):
        star_arg = StarArg(self.argument_control)
        self.star_args.append(star_arg)
        self.sizer.Insert(len(self.sizer.GetChildren()), star_arg, 0,
                          wx.EXPAND | wx.ALL, border=5)