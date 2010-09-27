import wx

from garlicsim.general_misc.third_party import inspect

from .opening_bracket import OpeningBracket
from .state_placeholder import StatePlaceholder
from .history_browser_placeholder import HistoryBrowserPlaceholder
from .comma import Comma
from .arg import Arg
from .star_arg import StarArg
from .star_kwarg import StarKwarg
from .closing_bracket import ClosingBracket


class ArgumentList(wx.Panel):
    def __init__(self, step_profile_dialog, step_function=None):
        self.step_profile_dialog = step_profile_dialog
        self.gui_project = step_profile_dialog.gui_project
        
        wx.Panel.__init__(self, step_profile_dialog)
        
        self.font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        
        self.bold_font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        
        self.step_function = None
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.build_for_step_function(step_function)
        

        
    def build_for_step_function(self, step_function):
        if self.step_function == step_function:
            return
        self.DestroyChildren()
        
        arg_spec = inspect.getargspec(step_function)
        
        arg_dict = self.step_profile_dialog.step_functions_to_argument_dicts[
            step_function
        ]
        
        star_arg_list = self.step_profile_dialog.step_functions_to_star_args[
            step_function
        ]
        
        star_kwarg_dict = self.step_profile_dialog.step_functions_to_star_kwargs[
            step_function
        ]
        
        
        
        self.opening_bracket = OpeningBracket(self)
        
        self.main_h_sizer.Add(self.opening_bracket, 0,
                              wx.ALIGN_CENTER_HORIZONTAL | 0, border=5)
        
        
        self.placeholder = \
            StatePlaceholder(self) if not self.gui_project.simpack_grokker.\
            history_dependent else HistoryBrowserPlaceholder(self)
        
        self.main_h_sizer.Add(self.placeholder, 0,
                              wx.ALIGN_CENTER_HORIZONTAL | 0, border=5)
        
        
        self.args = []
        
        for i, arg_name in list(enumerate(arg_spec.args))[1:]:
            self.main_h_sizer.Add(Comma(self), 0, wx.ALIGN_CENTER_HORIZONTAL | 0,
                                  border=5)
            value = repr(arg_dict[arg_name])
            if not value and (arg_name in arg_spec.defaults):
                value = arg_dict[arg_name] = repr(arg_spec.defaults[i])
            arg = Arg(self, arg_name, value)            
            self.args.append(arg)
            self.main_h_sizer.Add(arg, 0, wx.ALIGN_CENTER_HORIZONTAL | 0, border=5)
        
        
        self.star_args = []
        
        if arg_spec.varargs:
            for star_arg_value in star_arg_list:
                self.main_h_sizer.Add(Comma(self), 0, wx.ALIGN_CENTER_HORIZONTAL | 0,
                                  border=5)
                star_arg = StarArg(self, repr(star_arg_value))
                self.star_args.append(star_arg)
                self.main_h_sizer.Add(star_arg, 0, wx.ALIGN_CENTER_HORIZONTAL | 0,
                                      border=5)
        
        
        self.star_kwargs = []
        
        if arg_spec.keywords:
            for name, value in star_kwarg_dict:
                self.main_h_sizer.Add(Comma(self), 0, wx.ALIGN_CENTER_HORIZONTAL | 0,
                                  border=5)
                star_kwarg = StarKwarg(self, name, repr(value))
                self.star_kwargs.append(star_kwarg)
                self.main_h_sizer.Add(star_kwarg, 0, wx.ALIGN_CENTER_HORIZONTAL | 0,
                                      border=5)
        
        self.closing_bracket = ClosingBracket(self)
        
        self.main_h_sizer.Add(self.closing_bracket, 0,
                              wx.ALIGN_CENTER_HORIZONTAL | 0, border=5)