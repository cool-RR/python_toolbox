# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StarKwargBox` class.

See its documentation for more details.
'''

from __future__ import with_statement

import wx

from garlicsim.general_misc import cute_inspect
from garlicsim_wx.general_misc import wx_tools

from .star_kwarg import StarKwarg
from .star_adder import StarAdder, EVT_STAR_ADDER_PRESSED


class StarKwargBox(wx.StaticBox):
    '''
    Static box for specifying `**kwargs` to the step function.
    
    Note that this static box is not the parent of the widgets it creates.
    '''
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control,
                              label='&Keyword arguments')
        self.HelpText = ('Allows you to set the values of additional '
                         'keyword arguments that the step function accepts. '
                         'You need to supply both the argument name and the '
                         'argument value.')
        
        self.SetMinSize(argument_control.box_size)
        self.SetMaxSize(argument_control.box_size)
        
        self.sizer = wx.StaticBoxSizer(self, wx.VERTICAL)
        
        self.sizer.SetMinSize(argument_control.box_size)
        
        self.step_function = step_function
        
        arg_spec = cute_inspect.getargspec(step_function)
        
        star_kwarg_dict = \
            argument_control.step_profile_dialog.step_functions_to_star_kwargs[
                step_function
            ]
        
        self.star_kwargs = []
        
        for name, value in star_kwarg_dict.iteritems():
            star_kwarg = StarKwarg(argument_control, self, name, value)
            self.star_kwargs.append(star_kwarg)
            self.sizer.Add(star_kwarg, 0, wx.EXPAND | wx.ALL, border=5)
            
        self.star_adder = StarAdder(argument_control)
        self.sizer.Add(self.star_adder, 0, wx.EXPAND | wx.ALL, border=5)
        
        self.Parent.Bind(EVT_STAR_ADDER_PRESSED, self._on_star_adder_pressed,
                         source=self.star_adder)
        
        
    def _on_star_adder_pressed(self, event):
        
        with wx_tools.window_tools.WindowFreezer(self.Parent.Parent):
            star_kwarg = StarKwarg(self.argument_control, self)
            star_kwarg.MoveBeforeInTabOrder(self.star_adder)
            star_kwarg.SetFocus()
            self.star_kwargs.append(star_kwarg)
            self.sizer.Insert(len(self.sizer.GetChildren()) - 1, star_kwarg, 0,
                              wx.EXPAND | wx.ALL, border=5)
            self.layout()

        
    def layout(self):

        with wx_tools.window_tools.WindowFreezer(self.Parent.Parent):
        
            self.Parent.main_h_sizer.Fit(self.Parent)
            self.Parent.Layout()
            self.Parent.Parent.main_v_sizer.Fit(self.Parent.Parent)
            self.Parent.Parent.Layout()
        
            
    def remove(self, star_kwarg):
        '''Remove a `StarKwarg` from this `StarKwargBox`.'''
        index = self.star_kwargs.index(star_kwarg)
        
        if index >= 1:
            place_to_put_focus_in = \
                self.star_kwargs[index - 1].value_text_ctrl
        elif len(self.star_kwargs) >= 2:
            place_to_put_focus_in = \
                self.star_kwargs[1].value_text_ctrl
        else:
            place_to_put_focus_in = self.star_adder
        
        with wx_tools.window_tools.WindowFreezer(self.Parent.Parent):
            self.star_kwargs.remove(star_kwarg)
            self.sizer.Remove(star_kwarg)
            star_kwarg.DestroyChildren()
            star_kwarg.Destroy()
            self.layout()
            
        place_to_put_focus_in.SetFocus()
        
        