import wx

from garlicsim.general_misc.third_party import inspect

from .star_kwarg import StarKwarg


class StarKwargBox(wx.StaticBox):
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control,
                              label='Additional keyword arguments')
        
        self.sizer = wx.StaticBoxSizer(self, wx.HORIZONTAL)
        
        self.step_function = step_function
        
        arg_spec = inspect.getargspec(step_function)
        
        star_kwarg_dict = \
            argument_control.step_profile_dialog.step_functions_to_star_kwargs[
                step_function
            ]
                
        
        self.star_kwargs = []
        
        for name, value in star_kwarg_dict:
            star_kwarg = StarKwarg(argument_control, name, repr(value))
            self.star_kwargs.append(star_kwarg)
            self.sizer.Add(star_kwarg, 0)
            
        empty_star_kwarg = StarKwarg(argument_control, '', '')
        self.star_kwargs.append(empty_star_kwarg)
        self.sizer.Add(empty_star_kwarg, 0)
        
        