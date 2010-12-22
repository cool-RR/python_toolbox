# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `StarAdder` class.

See its documentation for more details.
'''

import wx
import pkg_resources

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools

from . import images as __images_package
images_package = __images_package.__name__


@caching.cache()
def get_bitmap():
    '''Get the "+" bitmap used for the star adder button.'''

    stream = pkg_resources.resource_stream(
        images_package,
        'plus.png'
    )
    
    return wx.BitmapFromImage(
        wx.ImageFromStream(
            stream,
            wx.BITMAP_TYPE_ANY
        )
    )


wxEVT_STAR_ADDER_PRESSED = wx.NewEventType()
EVT_STAR_ADDER_PRESSED = wx.PyEventBinder(
    wxEVT_STAR_ADDER_PRESSED,
    1
)
'''Event saying that a star adder button was pressed.'''


class StarAdder(wx.BitmapButton):
    '''Button for adding an entry for another star-arg or star-kwarg.'''
    def __init__(self, argument_control):
        self.argument_control = argument_control
        
        wx.BitmapButton.__init__(self, argument_control, bitmap=get_bitmap())
                
        self.Bind(wx.EVT_BUTTON, self.on_button)
        
    def on_button(self, event):
        wx_tools.post_event(self, EVT_STAR_ADDER_PRESSED, source=self)
        event.Skip()
            
        
