# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various keys and strings that describe them.'''

import wx


is_mac = (wx.Platform == '__WXMAC__')
is_gtk = (wx.Platform == '__WXGTK__')
is_win = (wx.Platform == '__WXMSW__')


from .global_keys import menu_keys, enter_keys

if is_win:
    from .win_keys import (back_keys, back_key_string,
                           forward_keys, forward_key_string)
elif is_gtk:
    from .gtk_keys import (back_keys, back_key_string,
                           forward_keys, forward_key_string)
else:
    assert is_mac
    from .mac_keys import (back_keys, back_key_string,
                           forward_keys, forward_key_string)