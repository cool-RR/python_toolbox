import wx

from garlicsim.general_misc.third_party import inspect

from .star_kwarg import StarKwarg


class StarKwargBox(wx.StaticBox):
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control,
                              label='Additional keyword arguments')
        
        self.sizer = wx.StaticBoxSizer(self, wx.HORIZONTAL)
        
        
        self.step_function = None
        
        
        self.SetSizer(self.main_h_sizer)
        
        
        arg_spec = inspect.getargspec(step_function)
        
        
        star_kwarg_dict = self.step_profile_dialog.step_functions_to_star_kwargs[
            step_function
        ]
                
        
        self.star_kwargs = []
        
        if arg_spec.keywords:
            for name, value in star_kwarg_dict:
                self.main_h_sizer.Add(Comma(self), 0,
                                      wx.ALIGN_CENTER_HORIZONTAL)
                star_kwarg = StarKwarg(self, name, repr(value))
                self.star_kwargs.append(star_kwarg)
                self.main_h_sizer.Add(star_kwarg, 0,
                                      wx.ALIGN_CENTER_HORIZONTAL)
        
        self.closing_bracket = ClosingBracket(self)
        
        self.main_h_sizer.Add(self.closing_bracket, 0,
                              wx.ALIGN_CENTER_HORIZONTAL)