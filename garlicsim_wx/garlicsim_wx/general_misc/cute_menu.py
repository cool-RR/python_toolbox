import wx

class CuteMenu(wx.Menu):
    @staticmethod
    def add_menus(menus, title='', style=0):
    
        big_menu = wx.Menu(title, style)
    
        first_run = True
    
        for menu in menus:
            
            if not first_run:
                big_menu.AppendSeparator()
            else:
                first_run = False
                
            for item in menu.GetMenuItems():
                big_menu.AppendItem(item)