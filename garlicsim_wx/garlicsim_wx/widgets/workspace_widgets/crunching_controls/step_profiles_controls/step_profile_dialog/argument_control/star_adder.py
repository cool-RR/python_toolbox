import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools

from . import images as __images_package
images_package = __images_package.__name__


@caching.cache()
def get_bitmap():

    stream = pkg_resources.resource_stream(
        images_package,
        'plus.png'
    )
    
    return wx.BitmapFromImage(
        wx.ImageFromStream(
            stream,
            wx.BITMAP_TYPE_PNG
        )
    )


wxEVT_STAR_ADDER_PRESSED = wx.NewEventType()
EVT_STAR_ADDER_PRESSED = wx.PyEventBinder(
    wxEVT_STAR_ADDER_PRESSED,
    1
)


class StarAdder(wx.BitmapButton):
    def __init__(self, argument_control):
        self.argument_control = argument_control
        
        wx.BitmapButton.__init__(self, argument_control, bitmap=get_bitmap())
        
        self.Bind(wx.EVT_BUTTON, self.on_button)
        
    def on_button(self, event):
        wx_tools.post_event(self, EVT_STAR_ADDER_PRESSED, source=self)
        event.Skip()
            