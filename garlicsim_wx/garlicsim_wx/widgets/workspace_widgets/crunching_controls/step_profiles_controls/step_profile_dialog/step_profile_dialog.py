# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StepProfileDialog` class.

See its documentation for more details.
'''

from __future__ import with_statement

import collections

import wx

from garlicsim.general_misc import address_tools
from garlicsim.general_misc import cute_inspect
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.widgets.general_misc.cute_error_dialog import CuteErrorDialog

import garlicsim
import garlicsim_wx
from garlicsim.misc import StepProfile

from .static_function_text import StaticFunctionText
from .step_function_input import StepFunctionInput, step_function_help_text
from .argument_control import ArgumentControl, ResolveFailed
from .already_exists_dialog import AlreadyExistsDialog
from .step_functions_to_argument_dicts import StepFunctionsToArgumentDicts


class StepProfileDialog(CuteDialog):
    '''Dialog for creating a new step profile, possibly from template.'''
    
    def __init__(self, step_profiles_controls, step_profile=None,
                 and_fork=False):
        '''
        Construct the `StepProfileDialog`.
        
        If given a `step_profile`, use it as a template. If it's `None`, start
        from scratch. Set `and_fork=True` if you intend to fork right after
        getting the step profile, though note it will only affect the labels;
        the actual forking is not done here.
        '''
        
        self.step_profiles_controls = step_profiles_controls
        
        self.gui_project = step_profiles_controls.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.frame = step_profiles_controls.frame
        
        self.and_fork = and_fork
        
        self.simpack = self.gui_project.simpack
        
        self.simpack_grokker = simpack_grokker = \
            self.gui_project.simpack_grokker
        
        title = 'Create a new step profile' if not and_fork else \
                'Create a new step profile and fork with it'
        CuteDialog.__init__(self, step_profiles_controls.GetTopLevelParent(),
                            title=title)
        
        self.original_step_profile = original_step_profile = step_profile
        
        del step_profile        
        
        
        self.hue = self.gui_project.step_profiles_to_hues.default_factory()
        
        self.step_functions_to_argument_dicts = \
            StepFunctionsToArgumentDicts(self.describe)
        
        self.step_functions_to_star_args = \
            collections.defaultdict(lambda: [])
        
        self.step_functions_to_star_kwargs = \
            collections.defaultdict(lambda: {})

        
        if original_step_profile:
            
            original_step_function = original_step_profile.step_function

            self.step_function = original_step_function
            
            initial_step_function_address = self.describe(
                original_step_function
            )

            original_argument_dict = collections.defaultdict(
                lambda: '',
                original_step_profile.getcallargs_result
            )

            self.step_functions_to_argument_dicts[original_step_function] = \
                dict((key, self.describe(value)) for (key, value) in
                 original_argument_dict.iteritems())
            

            original_arg_spec = cute_inspect.getargspec(original_step_function)
            
            
            if original_arg_spec.varargs:
                star_args_value = original_step_profile.getcallargs_result[
                    original_arg_spec.varargs
                ]
                
                self.step_functions_to_star_args[original_step_function] = \
                    [self.describe(value) for value in
                     star_args_value]
            
            
            if original_arg_spec.keywords:
                star_kwargs_value = original_step_profile.getcallargs_result[
                    original_arg_spec.keywords
                ]
                
                self.step_functions_to_star_kwargs[original_step_function] = \
                    dict((key, self.describe(value)) for (key, value)
                         in star_kwargs_value.iteritems())
                
            
            
            
        else:
            
            self.step_function = None
            
            if len(simpack_grokker.all_step_functions) >= 2:
                initial_step_function_address = ''
            else: # len(simpack_grokker.all_step_functions) == 1
                initial_step_function_address = self.describe(
                    simpack_grokker.default_step_function
                )
        
            
        #######################################################################
        # Setting up widgets and sizers:
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)

        
        
        self.static_text = wx.StaticText(self,
                                         label='Choose a step &function:')
        self.static_text.HelpText = step_function_help_text
        
        self.main_v_sizer.Add(self.static_text,
                              0,
                              wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
                              border=10)
        
        
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
                help_text=('Shows the hue of the to-be-created step profile. '
                           'Click to change.'),
                size=(25, 20)
            )
        
        self.h_sizer.Add(
            self.hue_control,
            0,
            wx.ALIGN_CENTER_VERTICAL
        )
        
        
        self.h_sizer.AddSpacer(5)
        
        
        self.step_function_input = StepFunctionInput(
            self,
            value=initial_step_function_address
        )
        
        self.h_sizer.Add(
            self.step_function_input,
            0,
            wx.ALIGN_CENTER_VERTICAL,
        )
        
        
        self.static_function_text = StaticFunctionText(
            self,
            step_function=original_step_function if original_step_profile \
                          else None
        )
        
        self.h_sizer.Add(
            self.static_function_text,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.LEFT,
            border=15
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
        
        ok_title = 'Create &step profile' if not and_fork else \
                   'Create &step profile and fork with it'
        self.ok_button = wx.Button(self, wx.ID_OK, ok_title)
        self.ok_button.HelpText = 'Create the new step profile.' if not \
            and_fork else 'Create the new step profile and fork with it.'
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.dialog_button_sizer.Realize()
    
        
        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
        self.bind_event_handlers(StepProfileDialog)
        
        # Finished setting up sizers and widgets.
        #######################################################################
    
        
    def set_step_function(self, step_function):
        '''Set the step function to be used in our new step profile.'''
        if step_function != self.step_function:
            with self.freezer: 
                self.step_function = step_function
                self.static_function_text.set_step_function(step_function)
                self.argument_control.set_step_function(step_function)
        elif step_function != self.static_function_text.step_function:
            self.static_function_text.set_step_function(step_function)
        
        
    def describe(self, step_function):
        '''Describe `step_function` as a string.'''
        return address_tools.describe(
            step_function,
            shorten=True,
            root=self.simpack,
            namespace=self.gui_project.namespace
        )
        
    
    def resolve(self, address):
        '''Resolve `address` into a Python object.'''
        return address_tools.resolve(
            address,
            root=self.simpack,
            namespace=self.gui_project.namespace
        )

    
    def ShowModal(self):
        wx.CallAfter(self.step_function_input.try_to_parse_text_and_set)
        self.step_function_input.SetFocus()
        return super(StepProfileDialog, self).ShowModal()
    
    
    def _on_ok_button(self, event):
        try:
            self.step_function_input.parse_text_and_set()
        except Exception, exception:
            CuteErrorDialog.create_and_show_modal(self,
                                              exception.args[0])
            self.step_function_input.SetFocus()
            return
        
        try:
            self.argument_control.save()
        except ResolveFailed, resolve_failed_exception:
            CuteErrorDialog.create_and_show_modal(self,
                                              resolve_failed_exception.message)
            resolve_failed_exception.widget.SetFocus()
            return

        step_function = self.step_function
        
        arg_spec = cute_inspect.getargspec(step_function)
        
        step_profile = StepProfile.create_from_dld_format(
            
            step_function,
            
            dict((key, self.resolve(value_string)) for 
                 (key, value_string) in self.\
                 step_functions_to_argument_dicts[step_function].iteritems()
                 if key in arg_spec.args),
            
            [self.resolve(value_string) for value_string in 
             self.step_functions_to_star_args[step_function]],
            
            dict((key, self.resolve(value_string)) for 
                 (key, value_string) in
                 self.step_functions_to_star_kwargs[step_function].iteritems())
        )
        
        
        if step_profile in self.gui_project.step_profiles:
            result = AlreadyExistsDialog.create_and_show_modal(
                self,
                step_profile,
                and_fork=self.and_fork
            )
            if result == wx.ID_OK:
                self.step_profile = step_profile
                self.EndModal(wx.ID_CANCEL)
                return
            else:
                assert result == wx.ID_CANCEL
                return
        else: # step_profile not in self.gui_project.step_profiles
            self.step_profile = step_profile
                
        self.EndModal(wx.ID_OK)
    
    
    def _on_cancel_button(self, event):
        # ...
        self.step_profile = None
        self.EndModal(wx.ID_CANCEL)
        
                         
        