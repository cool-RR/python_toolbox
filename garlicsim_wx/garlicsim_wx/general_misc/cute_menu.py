# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `CuteMenu` class.

See its documentation for more information.
'''

import wx
from garlicsim.general_misc.third_party import abc


class CuteMenu(wx.Menu):
    '''Menu class that allows easy adding of menus.'''
    
    __metaclass__ = abc.ABCMeta
        
    @abc.abstractmethod
    def _build(self):
        '''Build the menu, populating it with items and/or submenus.'''
    
    @staticmethod
    def add_menus(menus):
        '''
        Build a menu from a sequence of smaller menus.
        
        A separator will come between the items of one menu to the the items of
        the next.
        '''
        big_menu = UnbuildableCuteMenu()
    
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
                
        return big_menu
    
    
    def enable_in_menu_bar(self, enable=True):
        '''Enable (or disable) this menu in its containing menu bar.'''
        menu_bar = self.GetMenuBar()
        menu_bar.EnableTop(
            self._get_number_in_menu_bar(),
            enable
        )
        
        
    def _get_number_in_menu_bar(self):
        '''Get the index number of this menu in its containing menu bar.'''
        # todo: check if we even have a menu bar, otherwise throw helpful
        # exception.
        menu_bar = self.GetMenuBar()
        for (i, (menu, title)) in enumerate(menu_bar.GetMenus()):
            if menu is self:
                return i
        raise Exception
    
    
class UnbuildableCuteMenu(CuteMenu):
    '''
    CuteMenu that can't be built.
    
    This is useful when creating a Menu with `CuteMenu.add_menus`.
    '''
    def _build(self):
        raise Exception("Can't _build an UnbuildableCuteMenu.")