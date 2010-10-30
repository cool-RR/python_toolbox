from garlicsim_wx.widgets.general_misc.third_party import hypertreelist
from garlicsim_wx.widgets.general_misc.third_party import customtreectrl
from garlicsim_wx.widgets.general_misc.third_party.hypertreelist import *

from garlicsim_wx.general_misc import wx_tools


EVT_COMMAND_TREE_ITEM_RIGHT_CLICK = \
    wx.PyEventBinder(wx.wxEVT_COMMAND_TREE_ITEM_RIGHT_CLICK, 1)


class CuteHyperTreeList(HyperTreeList):
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, agwStyle=wx.TR_DEFAULT_STYLE,
                 validator=wx.DefaultValidator, name="HyperTreeList"):
        HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle,
                               validator, name)
        
        # Hackishly generating context menu event and tree item menu event from
        # these events:
        self.GetMainWindow().Bind(EVT_COMMAND_TREE_ITEM_RIGHT_CLICK,
                                  self.__on_command_tree_item_right_click)
        self.GetMainWindow().Bind(wx.EVT_KEY_DOWN, self.__on_key_down)
        self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.__on_right_up)
        self.GetMainWindow().Bind(wx.EVT_CONTEXT_MENU, self.__on_context_menu)

        
    
        
    def __on_command_tree_item_right_click(self, event):
        
        new_event = hypertreelist.TreeEvent(
            customtreectrl.wxEVT_TREE_ITEM_MENU,
            self.GetId(),
            item=event.GetItem(),
            point=self.ClientToScreen(event.GetPoint())
        )
        new_event.SetEventObject(self)
        wx.PostEvent(self, new_event)
        
        
    def _point_to_item(self, point):
        return self._main_win._anchor.HitTest(
            wx.Point(*point),
            self._main_win,
            0,
            self._main_win._curColumn,
            0
        )[0]

    
    def __on_right_up(self, event):
        item = self._point_to_item(
            self._main_win.CalcUnscrolledPosition(
                event.GetPosition()
            )
        )
        if item:
            assert item is self.GetSelection()
            
            new_event = hypertreelist.TreeEvent(
                customtreectrl.wxEVT_TREE_ITEM_MENU,
                self.GetId(),
                item=item,
                point=self.ClientToScreen(event.GetPosition())
            )
            new_event.SetEventObject(self)
            wx.PostEvent(self, new_event)
            
        else:
            new_event = wx.ContextMenuEvent(
                wx.wxEVT_CONTEXT_MENU,
                self.GetId(),
                self.ClientToScreen(event.GetPosition())
            )
            new_event.SetEventObject(self)
            wx.PostEvent(self, new_event)
            #wx_tools.post_event(self, wx.EVT_CONTEXT_MENU, self, meow='qw')
        
            
    def __on_key_down(self, event):
        # Hacky, either the OS or wxPython should be doing this:
        key = wx_tools.Key.get_from_key_event(event)
        if key in wx_tools.menu_keys:
            selection = self.GetSelection()
            if selection is not None:
                
                new_event = hypertreelist.TreeEvent(
                    customtreectrl.wxEVT_TREE_ITEM_MENU,
                    self.GetId(),
                    item=selection,
                )
                new_event.SetEventObject(self)
                self.GetEventHandler().ProcessEvent(new_event)
                
            else:
                wx_tools.post_event(self, wx.EVT_CONTEXT_MENU, self)
        else:
            event.Skip()


    def __on_context_menu(self, event):
        abs_position = event.GetPosition()
        position = abs_position - self.ScreenPosition
        selected_item = self.GetSelection()
        hit_item = self._point_to_item(position)
        
        if hit_item and (hit_item != selected_item):
            self._main_win.SelectItem(hit_item)
            selected_item = self.GetSelection()
            assert hit_item == selected_item
            
        if selected_item:
            #event.Veto()
            new_event = hypertreelist.TreeEvent(
                customtreectrl.wxEVT_TREE_ITEM_MENU,
                self.GetId(),
                item=selected_item,
                point=(position + self.ScreenPosition)
            )
            new_event.SetEventObject(self)
            wx.PostEvent(self, new_event)
            return
        else:
            event.Skip()