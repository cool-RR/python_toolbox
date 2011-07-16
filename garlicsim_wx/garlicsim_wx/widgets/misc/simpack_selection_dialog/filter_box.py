# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `FilterBox` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_control import CuteControl
from garlicsim_wx.general_misc import wx_tools


filter_help_text = ('Type text in the filter box in order to filter the '
                    'simpacks. You will see only the simpacks that contain '
                    'the text that you typed. For example, type "Physics" '
                    'in order to see only Physics-related simpacks.')


class FilterBox(wx.SearchCtrl, CuteControl):
    '''Box in which you can type text to filter the displayed simpacks.'''
    
    def __init__(self, navigation_panel):
        '''Construct the `FilterBox`, using `navigation_panel` as parent.'''
        wx.SearchCtrl.__init__(
            self,
            navigation_panel,
        )
        self.navigation_panel = navigation_panel
        self.ShowCancelButton(True)
        self.SetDescriptiveText('')
        self.SetHelpText(filter_help_text)
        self.bind_event_handlers(FilterBox)

    
    filter_words = property(
        lambda self: self.Value.split(),
        doc='''The current filter words, e.g. `['physics', '3d', 'bodies']`.'''
    )
            
    
    def _on_text(self, event):
        self.navigation_panel.\
                             simpack_selection_dialog.simpack_tree.reload_tree(
            ensure_simpack_selected=True
        )
        
            
    def _on_text_enter(self, event):
        # Currently not used because `TE_PROCESS_ENTER` also causes Tab to stop
        # working for navigation on Windows. I couldn't solve this.
        self.navigation_panel.simpack_selection_dialog.simpack_tree.SetFocus()
        
    
    def _on_searchctrl_cancel_btn(self, event):
        self.Value = ''
        self.navigation_panel.\
                             simpack_selection_dialog.simpack_tree.reload_tree(
            ensure_simpack_selected=True
        )
    