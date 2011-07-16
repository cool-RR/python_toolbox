# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CodeLink` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

from .inner_code_link import InnerCodeLink
from .code_unavailable_notice import CodeUnavailableNotice


class CodeLink(CutePanel):
    '''
    Link to the selected simpack's source code.
    
    If unable to supply such a link, shows a "(Code unavailable)" static text.
    '''
    def __init__(self, technical_details_bar):
        '''
        Construct the `CodeLink`, using `technical_details_bar` as parent.
        '''
        self.technical_details_bar = technical_details_bar
        CutePanel.__init__(self, technical_details_bar)
        if wx_tools.is_gtk:
            self.BackgroundColour = self.Parent.BackgroundColour
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.inner_code_link = InnerCodeLink(self)
        self.sizer.Add(self.inner_code_link)

        self.code_unavailable_notice = CodeUnavailableNotice(self)
        self.sizer.Add(self.code_unavailable_notice)
        
        self.bind_event_handlers(CodeLink)
        self.Hide()
        
        
    def refresh(self):
        '''Show link to simpack's code, or "(Code unavailable)" notice.'''
        simpack_metadata = self.technical_details_bar.simpack_info_panel.\
                                      simpack_selection_dialog.simpack_metadata
        self.Show(simpack_metadata is not None)
        if simpack_metadata is not None:
            if simpack_metadata.contains_source_files and \
                                            not simpack_metadata.is_zip_module:
                self.inner_code_link.Show()
                self.code_unavailable_notice.Hide()
            else: # not simpack_metadata.contains_source_files
                self.inner_code_link.Hide()
                self.code_unavailable_notice.Show()
                if simpack_metadata.is_zip_module:
                    self.code_unavailable_notice.set_reason(
                        ' The code is imported from a zip archive.'
                    )
                else:
                    assert not simpack_metadata.contains_source_files
                    self.code_unavailable_notice.set_reason(
                        ' The code has been compiled to binary form.'
                    )
                
        
        