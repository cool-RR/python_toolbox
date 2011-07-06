# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CruncherSelectionDialog` class.

See its documentation for more details.
'''

import wx

from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.widgets.general_misc.cute_static_text import CuteStaticText
from garlicsim_wx.widgets.general_misc.cute_error_dialog import CuteErrorDialog

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
        
        self.general_text = CuteStaticText(
            self,
            label=("C&hoose a cruncher type to be used when crunching the "
                   "simulation. Your simulation will use the same algorithm "
                   "regardless of which cruncher you'll choose; the choice of "
                   "cruncher will affect how and where that algorithm will be "
                   "run.")
        )
        if wx_tools.is_gtk: # Circumventing a bug in GTK:
            self.add_accelerators(
                {(wx_tools.keyboard.Key('h', alt=True),
                  wx_tools.keyboard.Key('H', alt=True)):
                 self.general_text.Id}
            )
            self.Bind(wx.EVT_MENU,
                      lambda event: self.cruncher_list_box.SetFocus(),
                      source=self.general_text)
        
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
        self.cruncher_list_box.SetHelpText(
            'List of cruncher types from which you can choose.'
        )
        
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
        
        self.ok_button = wx.Button(self, wx.ID_OK, '&Switch cruncher type')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.dialog_button_sizer.Realize()
        
        self.SetSizer(self.main_v_sizer)
        self.Layout()
        self.general_text.Wrap(self.general_text.Size[0])
        self.main_v_sizer.Fit(self)
        
        self.bind_event_handlers(CruncherSelectionDialog)
        self.update()

        
    def _on_ok_button(self, event):
        #event.Skip()
        self.try_to_change_cruncher_type_and_end_modal()
        
        
    def _on_cruncher_list_box__listbox_dclick(self, event):
        event.Skip()
        self.try_to_change_cruncher_type_and_end_modal()
        

    def try_to_change_cruncher_type_and_end_modal(self):
        if self.cruncher_types_availability[self.selected_cruncher_type]:
            self.gui_project.project.crunching_manager.cruncher_type = \
                self.selected_cruncher_type
            self.gui_project.cruncher_type_changed_emitter.emit()
            self.EndModal(wx.ID_OK)
        else: # Selected cruncher type is unavailable
            CuteErrorDialog.create_and_show_modal(
                self,
                '`%s` is not available.' % self.selected_cruncher_type.__name__
            )
        
        
    def _on_cancel_button(self, event):
        self.EndModal(wx.ID_CANCEL)

        
    def _on_cruncher_list_box__listbox(self, event):
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