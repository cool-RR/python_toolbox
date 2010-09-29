import wx

from garlicsim.general_misc.third_party import inspect
from garlicsim.general_misc import address_tools
from garlicsim.misc import exceptions
from garlicsim_wx.general_misc import wx_tools

from .arg_box import ArgBox
from .star_arg_box import StarArgBox
from .star_kwarg_box import StarKwargBox
from .placeholder import Placeholder
from .exceptions import ResolveFailed


class ArgumentControl(wx.Panel):
    def __init__(self, step_profile_dialog, step_function=None):
        self.step_profile_dialog = step_profile_dialog
        self.gui_project = step_profile_dialog.gui_project
        
        wx.Panel.__init__(self, step_profile_dialog)
        
        self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.box_size = wx.Size(200, -1) if wx.Platform == '__WXMSW__' \
                        else wx.Size(250, -1) 
        
        self.step_function = None
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.set_step_function(step_function)
        

        
    def set_step_function(self, step_function):
        if self.step_function == step_function:
            return

        self.step_function = step_function

        self.main_h_sizer.Clear(deleteWindows=True)
        #self.DestroyChildren()
        
        arg_spec = inspect.getargspec(step_function)
        
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
                Placeholder(self, '(No named arguments)'),
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
                Placeholder(self, '(No additional positional arguments)'),
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
                Placeholder(self, '(No additional keyword arguments)'),
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
        
        step_profile_dialog = self.step_profile_dialog
        step_function = self.step_function

        
        arg_dict = step_profile_dialog.\
                 step_functions_to_argument_dicts[step_function]
        
        star_arg_list = step_profile_dialog.\
                      step_functions_to_star_args[step_function]
        
        star_kwarg_dict = step_profile_dialog.\
                        step_functions_to_star_kwargs[step_function]
        
        
        arg_dict.clear()
        for arg in self.arg_box.args:
            name = arg.name
            value_string = arg.get_value_string()
            try:
                value = address_tools.resolve(value_string)
            except Exception:
                raise ResolveFailed("Can't resolve '%s' to a Python "
                                    "object." % value_string, arg)
            arg_dict[name] = value