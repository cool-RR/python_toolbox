import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

class EditMenu(CuteMenu):
    def __init__(self, frame):
        super(EditMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
        
        self.undo_button = self.Append(
            wx.ID_UNDO,
            '&Undo\tCtrl+Z',
            ' Undo the last operation'
        )
        self.undo_button.Enable(False)
        
        
        self.redo_button = self.Append(
            wx.ID_REDO,
            '&Redo\tCtrl+Y',
            ' Redo the last operation that was undone'
        )
        self.redo_button.Enable(False)
        
        
        self.AppendSeparator()
        
                
        self.cut_button = self.Append(
            wx.ID_CUT,
            'Cu&t\tCtrl+X',
            ''' Cut the current selection, copying to the clipboard and \
deleting it from the simulation'''
        )
        self.cut_button.Enable(False)
        
                
        self.copy_button = self.Append(
            wx.ID_COPY,
            '&Copy\tCtrl+C',
            ' Copy the current selection to the clipboard'
        )
        self.copy_button.Enable(False)
        
                
        self.paste_button = self.Append(
            wx.ID_PASTE,
            '&Paste\tCtrl+V',
            ' Paste the content of the clipboard into the simulation'
        )
        self.paste_button.Enable(False)
        
                
        self.clear_button = self.Append(
            wx.ID_CLEAR,
            'Cl&ear\tDel',
            ' Delete the current selection'
        )
        self.clear_button.Enable(False)
        
        
        self.AppendSeparator()


        self.select_all_button = self.Append(
            wx.ID_SELECTALL,
            'Select &All\tCtrl+A',
            ' Select all the nodes'
        )
        self.select_all_button.Enable(False)
        
        
        self.deselect_button = self.Append(
            -1,
            '&Deselect\tCtrl+D',
            ' Deselect all the selected nodes'
        )
        self.deselect_button.Enable(False)
        
        
        self.invert_selection_button = self.Append(
            -1,
            'Invert selection\tCtrl+Shift+I',
            ''' Select all the nodes that aren't selected, and deselect \
those that are selected'''
        )
        self.invert_selection_button.Enable(False)
        
        
        self.AppendSeparator()
        
        
        self.merge_to_blocks_button = self.Append(
            -1,
            'Merge to blocks where possible',
            ' Merge adjacant nodes to blocks, where possible'
        )
        self.merge_to_blocks_button.Enable(False)
        
        
        self.AppendSeparator()
        
        
        self.preferences_button = self.Append(
            wx.ID_PREFERENCES,
            'Prefere&nces',
            " View and modify GarlicSim's program-wide preferences"
        )
        self.preferences_button.Enable(False)
        
                
