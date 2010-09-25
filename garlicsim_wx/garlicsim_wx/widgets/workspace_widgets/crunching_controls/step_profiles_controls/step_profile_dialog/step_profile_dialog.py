import wx

from garlicsim.general_misc import address_tools
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog

import garlicsim
import garlicsim_wx

from .static_function_text import StaticFunctionText
from .step_function_input import StepFunctionInput
from .argument_list import ArgumentList


class StepProfileDialog(CuteDialog):
    # tododoc: this class will be responsible for checking if the new step
    # profile is already present in the step_profiles set.
    
    def __init__(self, step_profiles_controls, step_profile=None):
        
        self.step_profiles_controls = step_profiles_controls
        
        self.gui_project = step_profiles_controls.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.simpack = self.gui_project.simpack
        
        self.simpack_grokker = simpack_grokker = \
            self.gui_project.simpack_grokker
        
        
        CuteDialog.__init__(self, step_profiles_controls.frame,
                            title='Create a new step profile')
        
        self.original_step_profile = original_step_profile = step_profile
        
        del step_profile        
        
        
        self.hue = self.gui_project.step_profiles_to_hues.default_factory()

        
        if original_step_profile:
            initial_step_function_address = self.step_function_to_address(
                original_step_profile.step_function
            )
        else:
            if len(simpack_grokker.all_step_functions) >= 2:
                initial_step_function_address = ''
            else: # len(simpack_grokker.all_step_functions) == 1
                initial_step_function_address = self.step_function_to_address(
                    simpack_grokker.default_step_function
                )
        
            
        #######################################################################
        # Setting up sizers and widgets:
        
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
            wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,            
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
            wx.ALIGN_TOP | wx.ALL,            
            border=5
        )
        
        
        self.step_function_input = StepFunctionInput(
            self,
            value=initial_step_function_address
        )
        
        self.h_sizer.Add(
            self.step_function_input,
            0,
            wx.ALIGN_TOP | wx.ALL,            
            border=5
        )
        
        
        self.argument_list = ArgumentList(self)
        
        self.h_sizer.Add(
            self.argument_list,
            1,
            wx.EXPAND | wx.RIGHT,
            border=15
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
    
        
    def set_step_function(self, step_function):
        self.step_function = step_function
        self.static_function_text.set_step_function(step_function)
        # tododoc update the argument list
        
        
    def step_function_to_address(self, step_function):
        return address_tools.get_address(
            step_function,
            root=self.simpack,
            shorten=True
        )
        
    
    def address_to_object(self, address):
        return address_tools.get_object_by_address(
            address,
            root=self.simpack,
            shorten=True
        )

    
    def on_ok(self, event):
        # ...
        self.step_profile = 7
        self.EndModal(wx.ID_OK)
    
    
    def on_cancel(self, event):
        # ...
        self.EndModal(wx.ID_CANCEL)
        
                         
        