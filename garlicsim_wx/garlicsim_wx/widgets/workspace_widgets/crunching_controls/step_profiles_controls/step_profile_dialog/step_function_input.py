# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StepFunctionInput` class.

See its documentation for more details.
'''

import types

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_window import CuteWindow

import garlicsim_wx
import garlicsim

from .argument_control import colors


step_function_help_text = ('The step function to be used for crunching the '
                           'simulation. You may type the name of a different '
                           'step function or choose one from the given '
                           'options.')


class StepFunctionInput(wx.ComboBox, CuteWindow):
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
        
        width = 250 if wx_tools.is_win else 300
            
        wx.ComboBox.__init__(self, step_profile_dialog, value=value,
                             choices=step_functions_list, size=(width, -1))
        self.HelpText = step_function_help_text
        
        self._original_background_color = self.GetBackgroundColour()
        
        self.error_mode = False
        
        self.bind_event_handlers(StepFunctionInput)

        
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
            
        
    def _on_text(self, event):
        self.try_to_parse_text_and_set()
        
        
    def _on_combobox(self, event):
        self.try_to_parse_text_and_set()
        
        
    def _on_kill_focus(self, event):
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
    
