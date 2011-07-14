# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ArgumentControl` class.

See its documentation for more details.
'''

import wx

from garlicsim.general_misc import cute_inspect
from garlicsim.general_misc import misc_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim_wx.general_misc import wx_tools

from .arg_box import ArgBox
from .star_arg_box import StarArgBox
from .star_kwarg_box import StarKwargBox
from .placeholder import Placeholder
from .exceptions import ResolveFailed


class ArgumentControl(CutePanel):
    '''Widget for specifying arguments to a step function.'''
    def __init__(self, step_profile_dialog, step_function=None):
        self.step_profile_dialog = step_profile_dialog
        self.gui_project = step_profile_dialog.gui_project
        
        wx.Panel.__init__(self, step_profile_dialog)
        
        self.set_good_background_color()
        
        self.box_size = wx.Size(200, -1) if wx_tools.is_win \
                        else wx.Size(250, -1) 
        
        self.step_function = None
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.set_step_function(step_function)
        
        
    def set_step_function(self, step_function):
        '''Set the step function for which we are specifying arguments.'''
        if self.step_function == step_function:
            return
        
        if self.step_function is not None:
            try:
                self.save()
            except ResolveFailed:
                pass

        self.step_function = step_function

        self.main_h_sizer.Clear(deleteWindows=True)
        
        arg_spec = cute_inspect.getargspec(step_function)
        
        step_profile_dialog = self.step_profile_dialog
        
        arg_dict = step_profile_dialog.\
                 step_functions_to_argument_dicts[step_function]
        
        star_arg_list = step_profile_dialog.\
                      step_functions_to_star_args[step_function]
        
        star_kwarg_dict = step_profile_dialog.\
                        step_functions_to_star_kwargs[step_function]
        
        
        if arg_spec.args[1:]: # Filtering the state which is always present
            self.arg_box = ArgBox(self, step_function)
            self.main_h_sizer.Add(self.arg_box.sizer, 0, wx.ALL, border=10)
        else:
            self.arg_box = None
            self.main_h_sizer.Add(
                Placeholder(self, 'named arguments'),
                0,
                wx.ALL,
                border=10
            )
            
        
        if arg_spec.varargs:
            self.star_arg_box = StarArgBox(self, step_function)
            self.main_h_sizer.Add(self.star_arg_box.sizer, 0, wx.ALL,
                                  border=10)
        else:
            self.star_arg_box = None
            self.main_h_sizer.Add(
                Placeholder(self, 'positional arguments'),
                0,
                wx.ALL,
                border=10
            )
                
            
        if arg_spec.keywords:
            self.star_kwarg_box = StarKwargBox(self, step_function)
            self.main_h_sizer.Add(self.star_kwarg_box.sizer, 0, wx.ALL,
                                  border=10)
        else:
            self.star_kwarg_box = None
            self.main_h_sizer.Add(
                Placeholder(self, 'keyword arguments'),
                0,
                wx.ALL,
                border=10
            )
            
        
        self.main_h_sizer.Fit(self)
        self.Layout()
        self.step_profile_dialog.main_v_sizer.Fit(self.step_profile_dialog)
        self.step_profile_dialog.Layout()
        
        
        self.step_profile_dialog.Refresh()
        

    def save(self):
        '''
        Save all arguments to the dialog, unless there's an error resolving.
        
        The arguments will be saved to the following attributes of the dialog:
        
         *  `.step_functions_to_argument_dicts[step_function]`
         *  `.step_functions_to_star_args[step_function]`
         *  `.step_functions_to_star_kwargs[step_function]`
        
        '''
        
        step_profile_dialog = self.step_profile_dialog
        step_function = self.step_function

        
        arg_dict = step_profile_dialog.\
            step_functions_to_argument_dicts[step_function]
        
        star_arg_list = step_profile_dialog.\
            step_functions_to_star_args[step_function]
        
        star_kwarg_dict = step_profile_dialog.\
            step_functions_to_star_kwargs[step_function]
        
        resolve_failed = None
        
        
        if self.arg_box:
            arg_dict.clear()
            for arg in self.arg_box.args:
                name = arg.name
                value_string = arg.get_value_string() 
                try:
                    # Not storing, just checking if it'll raise an error:
                    self.step_profile_dialog.resolve(value_string)
                except Exception:
                    if not resolve_failed:
                        resolve_failed = ResolveFailed(
                            "Can't resolve '%s' to a Python "
                            "object." % value_string,
                            arg.value_text_ctrl
                        )
                else:
                    arg_dict[name] = value_string
        
            
        if self.star_arg_box:
            del star_arg_list[:]
            for star_arg in self.star_arg_box.star_args:
                value_string = star_arg.get_value_string()
                try:
                    # Not storing, just checking if it'll raise an error:
                    self.step_profile_dialog.resolve(value_string)
                except Exception:
                    if not resolve_failed:
                        resolve_failed = ResolveFailed(
                            "Can't resolve '%s' to a Python "
                            "object." % value_string,
                            star_arg.value_text_ctrl
                        )
                else:
                    star_arg_list.append(value_string)
                
                    
        if self.star_kwarg_box:
            star_kwarg_dict.clear()
            for star_kwarg in self.star_kwarg_box.star_kwargs:
                name = star_kwarg.get_name_string()
                if not misc_tools.is_legal_ascii_variable_name(name):
                    if not resolve_failed:
                        resolve_failed = ResolveFailed(
                            "'%s' is not a legal name for a variable." % name,
                            star_kwarg.name_text_ctrl
                        )
                    continue
                value_string = star_kwarg.get_value_string()
                try:
                    # Not storing, just checking if it'll raise an error:
                    self.step_profile_dialog.resolve(value_string)
                except Exception:
                    if not resolve_failed:
                        resolve_failed = ResolveFailed(
                            "Can't resolve '%s' to a Python "
                            "object." % value_string,
                            star_kwarg.value_text_ctrl
                        )
                else:
                    star_kwarg_dict[name] = value_string
                
        
        if resolve_failed:
            raise resolve_failed