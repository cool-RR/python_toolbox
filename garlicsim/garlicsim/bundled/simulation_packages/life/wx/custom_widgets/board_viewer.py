# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx
import wx.lib.scrolledpanel as scrolled

import garlicsim_wx

'''
Defines the BoardViewer class.
'''

class BoardViewer(scrolled.ScrolledPanel,
                  garlicsim_wx.widgets.WorkspaceWidget):
    '''Widget for displaying a Life board.'''
    def __init__(self, frame):
              
        scrolled.ScrolledPanel.__init__(self, frame,
                                        style=wx.SUNKEN_BORDER)
        
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetupScrolling()
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)

        self.border_width = 1
        self.square_size = 7
        self.board = None
        
        self._buffer_bitmap = wx.EmptyBitmap(1, 1)
        
        self.gui_project.active_node_changed_emitter.add_output(
            lambda: self.set_board(self.gui_project.active_node.state.board)
        )

        self.redraw_needed_flag = True
        

        
    def unscreenify(self, x, y):
        '''Translate screen coordinates to board coordinates.'''
        if self.board is None:
            return None
        screen_tuple = self.CalcUnscrolledPosition(x, y)
        result = [(thing // (self.border_width + self.square_size)) for
                  thing in screen_tuple]
        if (0 <= result[0] < self.board.width) and \
           (0 <= result[1] < self.board.height):
            return tuple(result)
        else:
            return None

    def set_board(self, board):
        '''Set the board to be displayed.'''
        if board is not self.board:
            self.board = board
            self.redraw_needed_flag = True
            self.Refresh()
        
    def _get_size_from_board(self):
        if self.board:
            return (
                self.board.width * (self.square_size + self.border_width),
                self.board.height * (self.square_size + self.border_width)
            )
        else:
            return (1, 1)
        
    def _draw_buffer_bitmap(self):        
        
        board = self.board
        
        (w, h) = self._get_size_from_board()
        self._buffer_bitmap = wx.EmptyBitmap(w, h)
        
        dc = wx.MemoryDC(self._buffer_bitmap)
        
        
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush('#d4d0c8'))
        dc.DrawRectangle(0, 0, w, h)
        
        if board is None:
            dc.Destroy()
            return
        
        white_brush = wx.Brush('White')
        black_brush = wx.Brush('Black')
        rectangles = []
        brushes = []
        for x in xrange(board.width):
            for y in xrange(board.height):
                rectangles.append([(self.square_size + self.border_width) * x,
                                   (self.square_size + self.border_width) * y,
                                   self.square_size,
                                   self.square_size])
                brushes.append(black_brush if board.get(x,y) is True
                               else white_brush)

        for rect in rectangles:
            (rect[0], rect[1]) = self.CalcScrolledPosition((rect[0], rect[1]))

        transparent_pen = wx.Pen('#000000', 0, wx.TRANSPARENT)
        
        dc.DrawRectangleList(rectangles, transparent_pen, brushes)
        dc.Destroy()
        
    def on_paint(self, event):
        '''Paint event handler.'''
        
        if self.redraw_needed_flag is True:
            self._draw_buffer_bitmap()
            self.redraw_needed_flag = False
        
        event.Skip()
        
        dc = wx.PaintDC(self)

        dc.DrawBitmapPoint(self._buffer_bitmap, self.CalcScrolledPosition((0, 0)))
        
        dc.Destroy()
        
        (w, h) = self._get_size_from_board()
        self.SetVirtualSize((w, h))


    def on_size(self, event):
        '''Refresh the widget.'''
        self.Refresh()
        if event is not None:
            event.Skip()

    def on_mouse_event(self, event):
        '''Mouse event handler.'''
        
        if event.LeftDown():
            pos = event.GetPositionTuple()
            thing = self.unscreenify(*pos)
            if thing is not None:
                (x, y) = thing
                old_value = self.board.get(x,y)
                new_value = (not old_value)

                new_state = self.gui_project.editing_state()
                new_board = new_state.board
                new_board.set(x, y, new_value)
            
                self.redraw_needed_flag = True


        self.Refresh()
