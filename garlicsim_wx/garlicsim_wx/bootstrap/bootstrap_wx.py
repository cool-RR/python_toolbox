import wx
if not hasattr(wx.Object, 'is_atomically_pickleable'):
    wx.Object.is_atomically_pickleable = False