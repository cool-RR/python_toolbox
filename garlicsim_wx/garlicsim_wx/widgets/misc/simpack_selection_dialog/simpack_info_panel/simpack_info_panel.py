# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackInfoPanel` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

from .name_display import NameDisplay
from .technical_details_bar import TechnicalDetailsBar
from .description_display import DescriptionDisplay
from .image_display import ImageDisplay


class SimpackInfoPanel(CutePanel):
    '''
    Panel showing information about the currently selected simpack.
    
    This includes its title, version number, description, tags, preview image,
    and a link to the simpack's source code.

    This panel wraps all of its subwidgets in a `wx.StaticBox` to make it clear
    that they are all part of a single group.
    '''
    
    def __init__(self, simpack_selection_dialog):
        '''Construct the `SimpackInfoPanel`.'''
        
        self.simpack_selection_dialog = simpack_selection_dialog
        CutePanel.__init__(self, simpack_selection_dialog)
        self.set_good_background_color()
        self.HelpText = ('This panel shows information about the '
                         'currently-selected simpack.')
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        
        self.static_box = wx.StaticBox(self)
        self.static_box_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)
        self.sizer.Add(self.static_box_sizer,
                       proportion=1,
                       flag=(wx.EXPAND | wx.RIGHT),
                       border=11)
        
        self.name_display = NameDisplay(self)
        self.static_box_sizer.Add(self.name_display,
                                  proportion=0,
                                  flag=(wx.ALIGN_LEFT | wx.BOTTOM),
                                  border=2)
        
        self.technical_details_bar = TechnicalDetailsBar(self)
        self.static_box_sizer.Add(self.technical_details_bar,
                                  proportion=0,
                                  flag=(wx.ALIGN_RIGHT | wx.BOTTOM),
                                  border=2)
        
        self.small_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.static_box_sizer.Add(self.small_h_sizer,
                                  proportion=1,
                                  flag=(wx.EXPAND))
        
        self.description_display = DescriptionDisplay(self)
        self.small_h_sizer.Add(self.description_display,
                               proportion=3,
                               flag=(wx.EXPAND | wx.RIGHT),
                               border=2)
        
        self.image_display = ImageDisplay(self)
        self.small_h_sizer.Add(self.image_display,
                               proportion=2,
                               flag=(wx.EXPAND))
        
        self.Layout()
         
        
    def refresh(self):
        '''
        Update all the widgets to show the currently-selected simpack-metadata.
        '''
        self.name_display.refresh()
        self.technical_details_bar.refresh()
        self.description_display.refresh()
        self.image_display.refresh()
        self.Refresh()
        self.Layout()