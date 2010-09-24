from garlicsim_wx.widgets.general_misc.third_party import hypertreelist
from garlicsim_wx.widgets.general_misc.third_party import customtreectrl
from garlicsim_wx.widgets.general_misc.third_party.hypertreelist import *

from garlicsim_wx.general_misc import wx_tools


EVT_COMMAND_TREE_ITEM_RIGHT_CLICK = \
    wx.PyEventBinder(wx.wxEVT_COMMAND_TREE_ITEM_RIGHT_CLICK, 1)


class CuteHyperTreeList(HyperTreeList):
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, agwStyle=wx.TR_DEFAULT_STYLE, validator=wx.DefaultValidator,
                 name="HyperTreeList"):
        HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle,
                               validator, name)
        
        # Hackishly generating context menu event and tree item menu event from
        # these three events:
        self.Bind(EVT_COMMAND_TREE_ITEM_RIGHT_CLICK,
                  self.on_command_tree_item_right_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)

        
    def on_command_tree_item_right_click(self, event):
        
        event = hypertreelist.TreeEvent(
            customtreectrl.wxEVT_TREE_ITEM_MENU,
            self.GetId(),
            item=event.GetItem()
        )
        event.SetEventObject(self)
        wx.PostEvent(self, event)
        
        
    def on_right_up(self, event):
        item = self._main_win._anchor.HitTest(
            self._main_win.CalcUnscrolledPosition(
                wx.Point(event.GetX(), event.GetY())
                ),
            self._main_win,
            0,
            self._main_win._curColumn,
            0
        )[0]
        if item:
            assert item is self.GetSelection()
            
            event = hypertreelist.TreeEvent(
                customtreectrl.wxEVT_TREE_ITEM_MENU,
                self.GetId(),
                item=item
            )
            event.SetEventObject(self)
            wx.PostEvent(self, event)
            #self.GetEventHandler().ProcessEvent(event)
            
        else:
            wx_tools.post_event(self, wx.EVT_CONTEXT_MENU, self)
        
            
    def on_key_down(self, event):
        # Hacky, either the OS or wxPython should be doing this:
        key = wx_tools.Key.get_from_key_event(event)
        if key in wx_tools.menu_keys:
            selection = self.GetSelection()
            if selection is not None:
                
                event = hypertreelist.TreeEvent(
                    customtreectrl.wxEVT_TREE_ITEM_MENU,
                    self.GetId(),
                    item=selection
                )
                event.SetEventObject(self)
                self.GetEventHandler().ProcessEvent(event)
                
            else:
                wx_tools.post_event(self, wx.EVT_CONTEXT_MENU, self)
        else:
            event.Skip()

