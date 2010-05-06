import wx

from file_menu import FileMenu
from edit_menu import EditMenu
from node_menu import NodeMenu
from block_menu import BlockMenu
from window_menu import WindowMenu
from help_menu import HelpMenu

class MenuBar(wx.MenuBar):
    def __init__(self, frame):
        super(MenuBar, self).__init__()
        self.frame = frame
        
        self.file_menu = FileMenu(frame)
        self.Append(self.file_menu, '&File')
        
        self.edit_menu = EditMenu(frame)
        self.Append(self.edit_menu, '&Edit')
        # This disables a menu from the bar:
        # self.EnableTop(self.FindMenu('Edit'), False)
        # Logically it makes sense, but it makes it hard to see all the options
        # in the menu, so at least for now I'm not doing it.
        
        self.node_menu = NodeMenu(frame)
        self.Append(self.node_menu, '&Node')
        self.node_menu._recalculate = lambda: self.EnableTop(
            self.FindMenu('Node'), 
            frame.gui_project is not None and \
            frame.gui_project.active_node is not None
        )
        
        self.block_menu = BlockMenu(frame)
        self.Append(self.block_menu, '&Block')
        self.block_menu._recalculate = lambda: self.EnableTop(
            self.FindMenu('Block'), 
            frame.gui_project is not None and \
            frame.gui_project.active_node is not None and \
            frame.gui_project.active_node.block is not None
        )
        
        self.window_menu = WindowMenu(frame)
        self.Append(self.window_menu, '&Window')
        
        self.help_menu = HelpMenu(frame)
        self.Append(self.help_menu, '&Help')