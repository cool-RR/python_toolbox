import wx

from garlicsim.general_misc.third_party import inspect

from .opening_bracket import OpeningBracket
from .state_placeholder import StatePlaceholder
from .history_browser_placeholder import HistoryBrowserPlaceholder
from .arg import Arg
from .star_arg import StarArg
from .star_kwarg import StarKwarg
from .closing_bracket import ClosingBracket


class ArgumentList(wx.Panel):
    def __init__(self, step_profile_dialog, step_function=None):
        self.step_profile_dialog = step_profile_dialog
        self.gui_project = step_profile_dialog.gui_project
        
        wx.Panel.__init__(self, step_profile_dialog)
        
        self.step_function = None
        
        self.build_for_step_function(step_function)
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)

        
    def build_for_step_function(self, step_function):
        if self.step_function == step_function:
            return
        self.DestroyChildren()
        
        arg_spec = inspect.getargspec(step_function)
        
        arg_dict = self.step_profile_dialog.step_functions_to_argument_dicts[
            step_function
        ]
        
        self.opening_bracket = OpeningBracket(self)
        
        self.main_h_sizer.Add(self.opening_bracket, 0,
                              wx.ALIGN_BOTTOM | wx.ALL, border=5)
        
        
        self.placeholder = \
            StatePlaceholder(self) if not self.gui_project.simpack_grokker.\
            history_dependent else HistoryBrowserPlaceholder(self)
        
        self.main_h_sizer.Add(self.placeholder, 0,
                              wx.ALIGN_BOTTOM | wx.ALL, border=5)
        
        self.args = []
        
        for arg_name in arg_spec.args:
            isinstance(arg_dict, dict)
            value = arg_dict[arg_name]
            if not value and (arg_name in arg_spec.defaults):
                value = arg_dict[arg_name] = repr(arg_spec.defaults[arg_name])
            arg = Arg(self, arg_name, value)