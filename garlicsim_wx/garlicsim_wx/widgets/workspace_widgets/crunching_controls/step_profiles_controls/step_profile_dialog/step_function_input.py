import types

import wx

import garlicsim_wx
import garlicsim


class StepFunctionInput(wx.ComboBox):
    # tododoc: if hitting on step function and it's not in the list, add it as
    # last
    def __init__(self, step_profile_dialog, value):
        self.step_profile_dialog = step_profile_dialog
        self.simpack_grokker = step_profile_dialog.simpack_grokker
        step_functions_list = [
            step_profile_dialog.step_function_to_address(step_function) for
            step_function in self.simpack_grokker.all_step_functions
        ]
        
        # If there's an initial value from an existing step profile, make sure
        # it's first on the list:
        if value:
            try:
                del step_functions_list[value]
            except Exception:
                pass
            step_functions_list.insert(0, value)
        
        width = 250 if wx.Platform == '__WXMAC__' else 150
            
        wx.ComboBox.__init__(self, step_profile_dialog, value=value,
                             choices=step_functions_list, size=(width, -1))
        
        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_box)
        
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)
        
        self.try_to_parse_text_and_set()

        
    def try_to_parse_text_and_set(self):
        text = str(self.GetValue())
        try:
            thing = self.step_profile_dialog.address_to_object(text)
        except Exception:
            return
        else:
            try:
                garlicsim.misc.simpack_grokker.get_step_type(thing)
            except Exception:
                return
            else:
                self.step_profile_dialog.set_step_function(thing)
                
    
    def parse_text_and_set(self):
        text = str(self.GetValue())
        try:
            thing = self.step_profile_dialog.address_to_object(text)
        except Exception:
            raise Exception("Unable to resolve '%s' into a step function." \
                            % text)
        else:
            try:
                step_type = garlicsim.misc.simpack_grokker.get_step_type(thing)
            except Exception:
                if callable(thing):
                    type_description = 'function' if \
                                     isinstance(thing, types.FunctionType) \
                                     else 'callable'
                    raise Exception("`%s` is a %s, but it's not a step "
                                    "function." % (text, type_description))
                else:
                    raise Exception("`%s` is a not a step function; It's not "
                                    "even a callable." % text)
            else:
                self.step_profile_dialog.set_step_function(thing)
            
        
    def on_text(self, event):
        self.try_to_parse_text_and_set()
    
        
    def on_combo_box(self, event):
        self.try_to_parse_text_and_set()
        
        
    def on_kill_focus(self, event):
        try:
            self.parse_text_and_set()
        except Exception as exception:
            self.step_profile_dialog.static_function_text.set_error_text(
                exception.message
            )
        event.Skip()