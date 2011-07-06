# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StarAdder` class.

See its documentation for more details.
'''

import wx
import pkg_resources

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_bitmap_button import \
                                                               CuteBitmapButton

from . import images as __images_package
images_package = __images_package.__name__


@caching.cache()
def get_bitmap():
    '''Get the "+" bitmap used for the star adder button.'''
    return wx_tools.bitmap_tools.bitmap_from_pkg_resources(
        images_package,
        'plus.png'
    )


wxEVT_STAR_ADDER_PRESSED = wx.NewEventType()
EVT_STAR_ADDER_PRESSED = wx.PyEventBinder(
    wxEVT_STAR_ADDER_PRESSED,
    1
)
'''Event saying that a star adder button was pressed.'''


class StarAdder(CuteBitmapButton):
    '''Button for adding an entry for another star-arg or star-kwarg.'''
    def __init__(self, argument_control):
        self.argument_control = argument_control
        CuteBitmapButton.__init__(
            self,
            argument_control,
            bitmap=get_bitmap(),
            tool_tip='Add another argument.',
            help_text='Add another argument.',
        )
        self.bind_event_handlers(StarAdder)
        
    def _on_button(self, event):
        wx_tools.event_tools.post_event(
            self,
            EVT_STAR_ADDER_PRESSED,
            source=self
        )
        event.Skip()
            
        
