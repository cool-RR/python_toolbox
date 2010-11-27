import wx
if not hasattr(wx.Object, '_is_atomically_pickleable'):
    wx.Object._is_atomically_pickleable = False