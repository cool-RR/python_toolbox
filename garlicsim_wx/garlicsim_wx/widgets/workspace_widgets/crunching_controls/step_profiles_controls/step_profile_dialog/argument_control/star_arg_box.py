import wx

from garlicsim.general_misc.third_party import inspect

from .star_arg import StarArg
from .star_adder import StarAdder, EVT_STAR_ADDER_PRESSED

# Note the most confusing thing about this class (and it's two brothers): It's
# not really the parent of the widgets it creates. This cost me many hours.
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
        
        for star_arg_value in star_arg_list + ['qwe']:
            star_arg = StarArg(argument_control, repr(star_arg_value))
            self.star_args.append(star_arg)
            self.sizer.Add(star_arg, 0, wx.EXPAND | wx.ALL, border=5)
            
        self.star_adder = StarAdder(argument_control)
        self.sizer.Add(self.star_adder, 0, wx.EXPAND | wx.ALL, border=5)
        
        self.Parent.Bind(EVT_STAR_ADDER_PRESSED, self.on_star_adder_pressed,
                         source=self.star_adder)
        
    def on_star_adder_pressed(self, event):
        star_arg = StarArg(self.argument_control)
        self.star_args.append(star_arg)
        self.sizer.Insert(len(self.sizer.GetChildren()), star_arg, 0,
                          wx.EXPAND | wx.ALL, border=5)
        
        self.Layout()