# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `StepFunctionInput` class.

See its documentation for more details.
'''

import types

import wx

import garlicsim_wx
import garlicsim

from .argument_control import colors


class StepFunctionInput(wx.ComboBox):
    '''
    Widget for specifying a step function.
    
    The step function is usually specified with the dropdown menu, but if it
    isn't in the simpack, it can be specified by typing in its address.
    '''
    def __init__(self, step_profile_dialog, value):
        self.step_profile_dialog = step_profile_dialog
        self.simpack_grokker = step_profile_dialog.simpack_grokker
        step_functions_list = [
            step_profile_dialog.describe(step_function) for
            step_function in self.simpack_grokker.all_step_functions
        ]
        
        # If there's an initial value from an existing step profile, make sure
        # it's first on the list:
        if value:
            if value in step_functions_list:
                step_functions_list.remove(value)
            step_functions_list.insert(0, value)
        
        width = 250 if wx.Platform == '__WXMSW__' else 300
            
        wx.ComboBox.__init__(self, step_profile_dialog, value=value,
                             choices=step_functions_list, size=(width, -1))
        
        self._original_background_color = self.GetBackgroundColour()
        
        self.error_mode = False
        
        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_box)
        
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)

        
    def select_step_function(self, step_function, step_function_string):
        '''
        Select `step_function`, with `step_function_string` being its address.
        '''
        if step_function_string not in self.GetItems():
            self.Append(step_function_string)
        self.step_profile_dialog.set_step_function(step_function)
        
        
    def try_to_parse_text_and_set(self):
        text = str(self.GetValue())
        try:
            thing = self.step_profile_dialog.resolve(text)
        except Exception:
            if self.error_mode:
                self._set_error_background()
            return
        else:
            step_type = garlicsim.misc.simpack_grokker.step_type.BaseStep.\
                      get_step_type(thing)
            if step_type:
                self.select_step_function(thing, text)
                if self.error_mode:
                    self._set_normal_background()
            else:
                assert step_type is None
                if self.error_mode:
                    self._set_error_background()
                return
                
                
    
    def parse_text_and_set(self):
        text = str(self.GetValue())
        try:
            thing = self.step_profile_dialog.resolve(text)
        except Exception:
            raise Exception("Error: Unable to resolve '%s' into a step "
                            "function." % text)
        else:
            step_type = garlicsim.misc.simpack_grokker.step_type.BaseStep.\
                      get_step_type(thing)
            if step_type:
                self.select_step_function(thing, text)
            else:
                assert step_type is None
                if callable(thing):
                    type_description = 'function' if \
                                     isinstance(thing, types.FunctionType) \
                                     else 'callable'
                    raise Exception("Error: `%s` is a %s, but it's not a step "
                                    "function." % (text, type_description))
                else:
                    raise Exception("Error `%s` is a not a step function; "
                                    "It's not even a callable." % text)
            
        
    def on_text(self, event):
        self.try_to_parse_text_and_set()
        
        
    def on_combo_box(self, event):
        self.try_to_parse_text_and_set()
        
        
    def on_kill_focus(self, event):
        event.Skip()
        if self.FindFocus() != self:
            try:
                self.parse_text_and_set()
            except Exception, exception:
                self.step_profile_dialog.static_function_text.set_error_text(
                    exception.args[0]
                )
                self.error_mode = True
                self._set_error_background()
            else:
                self._set_normal_background()

                
    def _set_error_background(self):
        '''Set the background of the control to an error color.'''
        self.SetBackgroundColour(colors.get_error_background_color())
        self.Refresh()
            
    
    def _set_normal_background(self):
        '''Set the background of the control to a non-error color.'''
        self.SetBackgroundColour(self._original_background_color)
        self.Refresh()
    
