# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `CruncherSelectionDialog` class.

See its documentation for more details.
'''

import wx

from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.widgets.general_misc.error_dialog import ErrorDialog

import garlicsim
import garlicsim_wx

from .cruncher_text_scrolled_panel import CruncherTextScrolledPanel


class CruncherSelectionDialog(CuteDialog):
    '''Dialog for changing the cruncher type used in the gui project.'''
    def __init__(self, cruncher_controls):
        CuteDialog.__init__(
            self,
            cruncher_controls.GetTopLevelParent(),
            title='Choose a cruncher type',
            size=(700, 300)
        )
        self.frame = cruncher_controls.frame
        self.gui_project = cruncher_controls.gui_project
        
        self.selected_cruncher_type = None
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.general_text = wx.StaticText(
            self,
            label=("Choose a cruncher type to be used when crunching the "
                   "simulation. Your simulation will use the same algorithm "
                   "regardless of which cruncher you'll choose; the choice of "
                   "cruncher will affect how and where that algorithm will be "
                   "run.")
        )
        #self.general_text.SetSize((self.ClientSize[0] - 20, -1))
        self.general_text.Wrap(self.ClientSize[0] - 20)
                                  
        self.general_text.Wrap(self.general_text.Size[0])
        
        self.main_v_sizer.Add(self.general_text, 0, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 0, wx.EXPAND)
        
        self.cruncher_types_availability = cruncher_types_availability = \
            self.gui_project.project.simpack_grokker.\
            cruncher_types_availability

        self.cruncher_titles = cruncher_titles = OrderedDict()
        
        for cruncher_type, availability in cruncher_types_availability.items():
            if availability == True:
                title = cruncher_type.__name__
            else:
                assert availability == False
                title = '%s (not available)' % cruncher_type.__name__
            cruncher_titles[title] = cruncher_type
        
        self.cruncher_list_box = wx.ListBox(
            self,
            choices=cruncher_titles.keys()
        )
        self.cruncher_list_box.SetMinSize((250, 100))
        
        self.cruncher_list_box.Select(
            cruncher_titles.values().index(
                self.gui_project.project.crunching_manager.cruncher_type
            )
        )
        
        self.h_sizer.Add(self.cruncher_list_box, 2*0, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.cruncher_text_scrolled_panel = CruncherTextScrolledPanel(self)
        
        self.h_sizer.Add(self.cruncher_text_scrolled_panel, 3*0,
                         wx.EXPAND | wx.ALL, border=10)
        
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        
        self.main_v_sizer.Add(self.dialog_button_sizer, 0,
                              wx.ALIGN_CENTER | wx.ALL, border=10)
        
        self.ok_button = wx.Button(self, wx.ID_OK, 'Switch cruncher type')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        self.dialog_button_sizer.Realize()
        
        
        self.Bind(wx.EVT_LISTBOX, self.on_list_box_change,
                  self.cruncher_list_box)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_list_box_double_click,
                  self.cruncher_list_box)
        
        self.SetSizer(self.main_v_sizer)
        self.Layout()
        self.general_text.Wrap(self.general_text.Size[0])
        self.main_v_sizer.Fit(self)
        
        self.update()

        
    def on_ok(self, event):
        #event.Skip()
        self.try_to_change_cruncher_type_and_end_modal()
        
        
    def on_list_box_double_click(self, event):
        event.Skip()
        self.try_to_change_cruncher_type_and_end_modal()
        

    def try_to_change_cruncher_type_and_end_modal(self):
        if self.cruncher_types_availability[self.selected_cruncher_type]:
            self.gui_project.project.crunching_manager.cruncher_type = \
                self.selected_cruncher_type
            self.gui_project.cruncher_type_changed_emitter.emit()
            self.EndModal(wx.ID_OK)
        else: # Selected cruncher type is unavailable
            error_dialog = ErrorDialog(
                self,
                '`%s` is not available.' % self.selected_cruncher_type.__name__
            )
            error_dialog.ShowModal()
            error_dialog.Destroy()
        
        
    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

        
    def on_list_box_change(self, event):
        self.update()
        
        
    def update(self):
        '''
        Update the text widget that explains about the current cruncher type.
        '''
        cruncher_types = self.cruncher_titles.values()
        selected_cruncher_type = cruncher_types[
            self.cruncher_list_box.GetSelection()
        ]
        if selected_cruncher_type is not self.selected_cruncher_type:
            self.selected_cruncher_type = selected_cruncher_type
            self.cruncher_text_scrolled_panel.update()
            
            
    def ShowModal(self):
        self.cruncher_list_box.SetFocus()
        return super(CruncherSelectionDialog, self).ShowModal()