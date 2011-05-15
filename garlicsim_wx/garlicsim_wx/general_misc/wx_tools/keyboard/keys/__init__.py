# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various keys and strings that describe them.'''

is_mac = (wx.Platform == '__WXMAC__')
is_gtk = (wx.Platform == '__WXGTK__')
is_win = (wx.Platform == '__WXMSW__')

if is_win:
    from .win_keys import ...
elif is_gtk:
    from .gtk_keys import ...
else:
    assert is_mac
    from .mac_keys import ...