
import webbrowser

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

class OnlineResourcesMenu(CuteMenu):
    def __init__(self, frame):
        super(OnlineResourcesMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
        
        self.website_button = self.Append(
            -1,
            'Official &website...',
            ' Open the official GarlicSim website in your browser'
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab('http://garlicsim.org'),
            self.website_button
        )
        
        
        self.mailing_lists_button = self.Append(
            -1,
            '&Mailing lists...',
            ''' Open the page with info about GarlicSim mailing lists\
in your browser'''
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab(
                'http://garlicsim.org/#mailing_lists'
                ),
            self.mailing_lists_button
        )
        
        
        self.blog_button = self.Append(
            -1,
            '&Blog...',
            ' Open the GarlicSim blog in your browser'
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab(
                'http://blog.garlicsim.org'
                ),
            self.blog_button
        )
        

        self.github_button = self.Append(
            -1,
            'Code &repository...',
            ' Open the GitHub code repository for GarlicSim in your browser'
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab(
                'http://github.com/cool-RR/GarlicSim'
                ),
            self.github_button
        )
                
