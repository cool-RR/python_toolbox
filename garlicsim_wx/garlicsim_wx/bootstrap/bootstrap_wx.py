import wx
if not hasattr(wx.Object, 'is_pickleable'):
    wx.Object.is_pickleable = False