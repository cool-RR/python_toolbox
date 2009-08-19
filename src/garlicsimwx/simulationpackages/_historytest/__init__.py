from historytest import *

try:
    import wx
    wx_installed = True
except ImportError:
    wx_installed = False

if wx_installed:
    from historytestgui import *