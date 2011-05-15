# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Key` class.

See its documentation for more information.
'''

import wx


class Key(object):    
    '''A key combination.'''

    def __init__(self, key_code, cmd=False, alt=False, shift=False):

        self.key_code = key_code        
        '''The numerical code of the pressed key.'''
        
        self.cmd = cmd
        '''Flag saying whether the ctrl/cmd key was pressed.'''
        
        self.alt = alt
        '''Flag saying whether the alt key was pressed.'''
        
        self.shift = shift
        '''Flag saying whether the shift key was pressed.'''
        
        
    @staticmethod
    def get_from_key_event(event):
        '''Construct a Key from a wx.EVT_KEY_DOWN event.'''
        return Key(event.GetKeyCode(), event.CmdDown(),
                   event.AltDown(), event.ShiftDown())
    
    def to_accelerator_pair(self):
        modifiers = (
            wx.ACCEL_NORMAL |
            (wx.ACCEL_CMD if self.cmd else wx.ACCEL_NORMAL) |
            (wx.ACCEL_ALT if self.alt else wx.ACCEL_NORMAL) |
            (wx.ACCEL_SHIFT if self.shift else wx.ACCEL_NORMAL)
        )
        
        return (modifiers, self.key_code)
         
    
    def __hash__(self):
        return hash(tuple(sorted(tuple(vars(self)))))
    
    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return self.key_code == other.key_code and \
               self.cmd == other.cmd and \
               self.shift == other.shift and \
               self.alt == other.alt
