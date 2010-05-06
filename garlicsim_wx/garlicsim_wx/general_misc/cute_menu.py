import wx

class CuteMenu(wx.Menu): # todo: make abc that enforces _build
    
    """
    def __init__(self):
        if not getattr(self, '_CuteMenu__parent_init_called', False):
            super(CuteMenu, self).__init__()
        self.__parent_init_called = True
    """
        
    @staticmethod
    def add_menus(menus):#, title='', style=0):
    
        big_menu = CuteMenu()#title, style)
    
        first_run = True
    
        for menu in menus:

            assert isinstance(menu, CuteMenu)
            
            if not first_run:
                big_menu.AppendSeparator()
                assert big_menu.frame is menu.frame
            else:
                big_menu.frame = menu.frame
                first_run = False
                
            type(menu).__dict__['_build'](big_menu)
            
            #for item in menu.GetMenuItems():
                #big_menu.AppendItem(item)
                
        return big_menu