# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ArgBox` class.

See its documentation for more details.
'''

import wx

from garlicsim.general_misc import cute_inspect

from .arg import Arg


class ArgBox(wx.StaticBox):    
    '''
    Static box for specifying arguments to the step function.
    
    Note that this static box is not the parent of the widgets it creates.
    '''
    def __init__(self, argument_control, step_function):
        self.argument_control = argument_control
        
        wx.StaticBox.__init__(self, argument_control, label='&Arguments',
                              size=argument_control.box_size)
        self.HelpText = ('Allows you to set the values of arguments that the '
                         'step function accepts.')
        
        self.SetMinSize(argument_control.box_size)
        self.SetMaxSize(argument_control.box_size)
        
        self.sizer = wx.StaticBoxSizer(self, wx.VERTICAL)
        
        self.sizer.SetMinSize(argument_control.box_size)
        
        self.step_function = step_function
        
        arg_spec = cute_inspect.getargspec(step_function)
        
        arg_dict = argument_control.step_profile_dialog.\
            step_functions_to_argument_dicts[
                step_function
            ]
        
        self.args = []
        
        for i, arg_name in list(enumerate(arg_spec.args))[1:]:
            value = arg_dict[arg_name]
            if not value and (arg_name in arg_spec.defaults):
                value = arg_dict[arg_name] = repr(arg_spec.defaults[i])
            arg = Arg(argument_control, arg_name, value)
            self.args.append(arg)
            self.sizer.Add(arg, 0, wx.EXPAND | wx.ALL, border=5)
            