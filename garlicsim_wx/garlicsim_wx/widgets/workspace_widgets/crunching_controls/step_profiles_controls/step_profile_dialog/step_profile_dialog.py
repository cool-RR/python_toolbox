import collections

import wx

from garlicsim.general_misc import address_tools
from garlicsim.general_misc.third_party import inspect
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.widgets.general_misc.error_dialog import ErrorDialog

import garlicsim
import garlicsim_wx

from .static_function_text import StaticFunctionText
from .step_function_input import StepFunctionInput
from .argument_control import ArgumentControl
from .already_exists_dialog import AlreadyExistsDialog
from .step_functions_to_argument_dicts import StepFunctionsToArgumentDicts


class StepProfileDialog(CuteDialog):
    # tododoc: this class will be responsible for checking if the new step
    # profile is already present in the step_profiles set.
    
    def __init__(self, step_profiles_controls, step_profile=None):
        
        self.step_profiles_controls = step_profiles_controls
        
        self.gui_project = step_profiles_controls.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.frame = step_profiles_controls.frame
        
        self.simpack = self.gui_project.simpack
        
        self.simpack_grokker = simpack_grokker = \
            self.gui_project.simpack_grokker
        
        
        CuteDialog.__init__(self, step_profiles_controls.frame,
                            title='Create a new step profile')
        
        self.original_step_profile = original_step_profile = step_profile
        
        del step_profile        
        
        
        self.hue = self.gui_project.step_profiles_to_hues.default_factory()
        
        self.step_functions_to_argument_dicts = \
            StepFunctionsToArgumentDicts()
        
        self.step_functions_to_star_args = \
            collections.defaultdict(lambda: [])
        
        self.step_functions_to_star_kwargs = \
            collections.defaultdict(lambda: {})

        
        if original_step_profile:
            original_step_function = original_step_profile.step_function
            initial_step_function_address = self.step_function_to_address(
                original_step_function
            )

            original_argument_dict = collections.defaultdict(
                lambda: '',
                original_step_profile.getcallargs_result
            )

            self.step_functions_to_argument_dicts[original_step_function] = \
                original_argument_dict
            

            original_arg_spec = inspect.getargspec(original_step_function)
            
            
            if original_arg_spec.varargs:
                star_args_value = original_step_profile.getcallargs_result[
                    original_arg_spec.varargs
                ]
                
                self.step_functions_to_star_args[original_step_function] = \
                    star_args_value
            
            
            if original_arg_spec.keywords:
                star_kwargs_value = original_step_profile.getcallargs_result[
                    original_arg_spec.keywords
                ]
                
                self.step_functions_to_star_kwargs[original_step_function] = \
                    star_kwargs_value
                
            
            
            
        else:
            if len(simpack_grokker.all_step_functions) >= 2:
                initial_step_function_address = ''
            else: # len(simpack_grokker.all_step_functions) == 1
                initial_step_function_address = self.step_function_to_address(
                    simpack_grokker.default_step_function
                )
        
            
        #######################################################################
        # Setting up widgets and sizers:
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        self.static_function_text = StaticFunctionText(self)
        
        self.main_v_sizer.Add(
            self.static_function_text,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,
            border=10
        )

        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(
            self.h_sizer,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,            
            border=10
        )
        

        self.hue_control = \
            garlicsim_wx.widgets.general_misc.hue_control.HueControl(
                self,
                lambda: getattr(self, 'hue'),
                lambda hue: setattr(self, 'hue', hue),
                emitter=None,
                lightness=0.8,
                saturation=1,
                dialog_title='Select hue for new step profile',
                size=(25, 20)
            )
        
        self.h_sizer.Add(
            self.hue_control,
            0,
            wx.ALIGN_TOP | wx.TOP,
            border=(5 if wx.Platform=='__WXMAC__' else 0)
        )
        
        
        self.h_sizer.AddSpacer(5)
        
        
        self.step_function_input = StepFunctionInput(
            self,
            value=initial_step_function_address
        )
        
        self.h_sizer.Add(
            self.step_function_input,
            0,
            wx.ALIGN_TOP,
            #border=5
        )
        
        
        self.argument_control = ArgumentControl(
            self,
            original_step_function if original_step_profile else None
        )
        
        self.main_v_sizer.Add(
            self.argument_control,
            1,
            wx.ALIGN_CENTER_HORIZONTAL | wx.TOP,
            border=0
        )
        
        
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        
        self.main_v_sizer.Add(
            self.dialog_button_sizer,
            0,
            wx.ALIGN_CENTER | wx.ALL,
            border=10
        )
        
        self.ok_button = wx.Button(self, wx.ID_OK, 'Create step profile')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        self.dialog_button_sizer.Realize()
    
        
        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
        
        # Finished setting up sizers and widgets.
        #######################################################################
        
        # wx.CallAfter(self.step_function_input.try_to_parse_text_and_set)
    
        
    def set_step_function(self, step_function):
        self.step_function = step_function
        self.static_function_text.set_step_function(step_function)
        self.argument_control.set_step_function(step_function)
        
        
    def step_function_to_address(self, step_function):
        return address_tools.get_address(
            step_function,
            root=self.simpack,
            shorten=True
        )
        
    
    def address_to_object(self, address):
        return address_tools.get_object_by_address(
            address,
            root=self.simpack
        )

    
    def on_ok(self, event):
        try:
            self.step_function_input.parse_text_and_set()
        except Exception as exception:
            error_dialog = ErrorDialog(self, exception.message)
            error_dialog.ShowModal()
            self.SetFocus(self.step_function_input)
            return
        # tododoc: add args:
        step_profile = garlicsim.misc.StepProfile(self.step_function)
        if step_profile in self.gui_project.step_profiles:
            dialog = AlreadyExistsDialog(self, step_profile)
            result = dialog.ShowModal() 
            if result == wx.ID_OK:
                self.EndModal(wx.ID_CANCEL)
                return
            else:
                assert result == wx.ID_CANCEL
                return
        else: # step_profile not in self.gui_project.step_profiles
            self.step_profile = step_profile
                
        self.EndModal(wx.ID_OK)
    
    
    def on_cancel(self, event):
        # ...
        self.EndModal(wx.ID_CANCEL)
        
                         
        