# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `HueSelectionDialog` class.

See its documentation for more details.
'''

# todo: should have validation in `Textual`, currently can enter words

import wx

from python_toolbox.wx_tools.widgets.cute_dialog import CuteDialog
from python_toolbox.emitting import Emitter

from .wheel import Wheel
from .textual import Textual


class HueSelectionDialog(CuteDialog):
    '''Dialog for changing a hue.'''

    def __init__(self, parent, getter, setter, emitter, lightness=1,
                 saturation=1, id=-1, title='Select hue',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr):


        CuteDialog.__init__(self, parent, id, title, pos, size, style, name)

        ### Defining attributes: ##############################################
        #                                                                     #
        self.getter = getter
        '''Getter function for getting the current hue.'''

        self.setter = setter
        '''Setter function for setting a new hue.'''

        assert isinstance(emitter, Emitter)
        self.emitter = emitter
        '''Optional emitter to emit to when changing hue. May be `None`.'''

        self.lightness = lightness
        '''The constant lightness of the colors that we're displaying.'''

        self.saturation = saturation
        '''The constant saturation of the colors that we're displaying.'''

        self.hue = getter()
        '''The current hue.'''

        self.old_hue = self.hue
        '''The hue as it was before changing, when the dialog was created.'''

        self.old_hls = (self.old_hue, lightness, saturation)
        '''
        The hls color as it was before changing, when the dialog was created.
        '''
        #                                                                     #
        ### Finished defining attributes. #####################################

        self.__init_build()

        self.emitter.add_output(self.update)


    def __init_build(self):
        '''Build the widget.'''
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_v_sizer.Add(self.h_sizer, 0)

        self.wheel = Wheel(self)
        self.h_sizer.Add(self.wheel, 0)

        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer.Add(self.v_sizer, 0, wx.ALIGN_CENTER)
        self.comparer = Comparer(self)
        self.v_sizer.Add(self.comparer, 0, wx.RIGHT | wx.TOP | wx.BOTTOM,
                         border=10)

        self.textual = Textual(self)
        self.v_sizer.Add(self.textual, 0, wx.RIGHT | wx.TOP | wx.BOTTOM,
                         border=10)

        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        self.main_v_sizer.Add(self.dialog_button_sizer, 0,
                              wx.ALIGN_CENTER | wx.ALL, border=10)

        self.ok_button = wx.Button(self, wx.ID_OK, '&Ok')
        self.ok_button.SetHelpText('Change to the selected hue.')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)

        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.cancel_button.SetHelpText('Change back to the old hue.')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.dialog_button_sizer.Realize()

        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
        self.bind_event_handlers(HueSelectionDialog)



    def update(self):
        '''If hue changed, update all widgets to show the new hue.'''
        self.hue = self.getter()
        self.wheel.update()
        self.comparer.update()
        self.textual.update()


    ### Overriding `wx.Dialog` methods: #######################################
    #                                                                         #
    def ShowModal(self):
        '''Show the dialog modally. Overridden to focus on `self.textual`.'''
        wx.CallAfter(self.textual.set_focus_on_spin_ctrl_and_select_all)
        return super().ShowModal()


    def Destroy(self):
        self.emitter.remove_output(self.update)
        super().Destroy()
    #                                                                         #
    ### Finished overriding `wx.Dialog` methods. ##############################

    ### Event handlers: #######################################################
    #                                                                         #
    def _on_ok_button(self, event):
        self.EndModal(wx.ID_OK)


    def _on_cancel_button(self, event):
        self.setter(self.old_hue)
        self.EndModal(wx.ID_CANCEL)
    #                                                                         #
    ### Finished event handlers. ##############################################


from .comparer import Comparer
