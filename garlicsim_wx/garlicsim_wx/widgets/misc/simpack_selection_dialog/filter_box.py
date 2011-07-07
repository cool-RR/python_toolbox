# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''
import wx

from garlicsim_wx.general_misc import emitters
from garlicsim_wx.widgets.general_misc.cute_control import CuteControl


filter_help_text = ('Type text in the filter box in order to filter the '
                    'simpacks. You will see only the simpacks that contain '
                    'the text that you typed. For example, type "Physics" '
                    'in order to see only Physics-related simpacks.')


class FilterBox(wx.SearchCtrl, CuteControl):
    def __init__(self, navigation_panel):
        wx.SearchCtrl.__init__(self, navigation_panel)
        self.navigation_panel = navigation_panel
        self.ShowCancelButton(True)
        self.SetDescriptiveText('')
        self.SetHelpText(filter_help_text)
        self.bind_event_handlers(FilterBox)
        self.filter_words = ''
        self.filter_words_changed_emitter = emitters.Emitter(
                name='filter_words_changed',
        )
    
        
    def _on_text(self, event):
        event.Skip()
        new_filter_words = self.Value.split()
        if new_filter_words != self.filter_words:
            self.filter_words = new_filter_words
            self.filter_words_changed_emitter.emit()

            
    def _on_searchctrl_search_btn(self, event):
        self.navigation_panel.simpack_selection_dialog.simpack_tree.SetFocus()