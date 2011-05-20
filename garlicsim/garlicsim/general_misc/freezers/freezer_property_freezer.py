# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from .freezer import Freezer

class FreezerPropertyFreezer(Freezer):
    ''' '''
    def __init__(self, thing):
        self.thing = thing
        
        
        
    def freeze_handler(self):
        return self.freezer_property._freeze_handler(self.thing)
    
    def thaw_handler(self):
        return self.freezer_property._thaw_handler(self.thing)