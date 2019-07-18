# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import wx


class Key:
    '''A key combination.'''

    def __init__(self, key_code, cmd=False, alt=False, shift=False):

        assert isinstance(key_code, int) or isinstance(key_code, str)
        self.key_code = key_code if isinstance(key_code, int) else \
                        ord(key_code)
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

    def is_alphanumeric(self):
        return (ord('0') <= self.key_code <= ord('9')) or \
               (ord('A') <= self.key_code <= ord('z'))


    def __str__(self):
        return chr(self.key_code)


    def __unicode__(self):
        return unichr(self.key_code)


    def __hash__(self):
        return hash(tuple(sorted(tuple(vars(self)))))


    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return self.key_code == other.key_code and \
               self.cmd == other.cmd and \
               self.shift == other.shift and \
               self.alt == other.alt


    def __ne__(self, other):
        return not self == other


    def __repr__(self):
        '''
        Get a string representation of the `Key`.

        Example output:

            <Key: Alt-Shift-K>

        ''' # todo: Make it work for key codes like `WXK_F12`.
        key_list = [chr(self.key_code)]
        if self.cmd:
            key_list.insert(0, 'Cmd')
        if self.shift:
            key_list.insert(0, 'Shift')
        if self.alt:
            key_list.insert(0, 'Alt')

        return '<%s: %s>' % \
               (
                   type(self).__name__,
                   '-'.join(key_list)
               )
