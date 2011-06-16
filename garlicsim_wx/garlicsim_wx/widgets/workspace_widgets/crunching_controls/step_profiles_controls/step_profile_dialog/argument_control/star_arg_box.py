# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StarArgBox` class.

See its documentation for more details.
'''

from __future__ import with_statement

import wx

from garlicsim.general_misc import cute_inspect
from garlicsim_wx.general_misc import wx_tools

from .star_arg import StarArg
from .star_adder import StarAdder, EVT_STAR_ADDER_PRESSED


class StarArgBox(wx.StaticBox):
    '''
    Static box for specifying extraneous args (`*args`) to the step function.
    
    Note that this static box is not the parent of the widgets it creates.
    '''
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control,
                              label='&Positional arguments')
        
        self.SetMinSize(argument_control.box_size)
        self.SetMaxSize(argument_control.box_size)
        
        self.sizer = wx.StaticBoxSizer(self, wx.VERTICAL)
        
        self.sizer.SetMinSize(argument_control.box_size)
        
        self.step_function = step_function
        
        arg_spec = cute_inspect.getargspec(step_function)
        
        star_arg_list = \
            argument_control.step_profile_dialog.step_functions_to_star_args[
                step_function
            ]
        
        
        self.star_args = []
        
        for star_arg_value in star_arg_list:
            star_arg = StarArg(argument_control, self, star_arg_value)
            self.star_args.append(star_arg)
            self.sizer.Add(star_arg, 0, wx.EXPAND | wx.ALL, border=5)
            
        self.star_adder = StarAdder(argument_control)
        self.sizer.Add(self.star_adder, 0, wx.EXPAND | wx.ALL, border=5)
        
        self.Parent.Bind(EVT_STAR_ADDER_PRESSED, self._on_star_adder_pressed,
                         source=self.star_adder)
        
        
    def _on_star_adder_pressed(self, event):
        
        with wx_tools.window_tools.WindowFreezer(self.Parent.Parent):
            star_arg = StarArg(self.argument_control, self)
            star_arg.MoveBeforeInTabOrder(self.star_adder)
            star_arg.SetFocus()
            self.star_args.append(star_arg)
            self.sizer.Insert(len(self.sizer.GetChildren()) - 1, star_arg, 0,
                              wx.EXPAND | wx.ALL, border=5)
            self.layout()

        
    def layout(self):

        with wx_tools.window_tools.WindowFreezer(self.Parent.Parent):
        
            self.Parent.main_h_sizer.Fit(self.Parent)
            self.Parent.Layout()
            self.Parent.Parent.main_v_sizer.Fit(self.Parent.Parent)
            self.Parent.Parent.Layout()
        
            
    def remove(self, star_arg):
        '''Remove a `StarArg` from this box.'''
        index = self.star_args.index(star_arg)
        
        if index >= 1:
            place_to_put_focus_in = \
                self.star_args[index - 1].value_text_ctrl
        elif len(self.star_args) >= 2:
            place_to_put_focus_in = \
                self.star_args[1].value_text_ctrl
        else:
            place_to_put_focus_in = self.star_adder
            
        with wx_tools.window_tools.WindowFreezer(self.Parent.Parent):
            self.star_args.remove(star_arg)
            self.sizer.Remove(star_arg)
            star_arg.DestroyChildren()
            star_arg.Destroy()
            self.layout()
        
        place_to_put_focus_in.SetFocus()