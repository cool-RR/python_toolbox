# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from .freezer import Freezer


class FreezerPropertyFreezer(Freezer):
    '''
    Freezer used internally by `FreezerProperty`.
    
    It uses the `FreezerProperty`'s internal freeze/thaw handlers as its own
    freeze/thaw handlers.
    '''
    
    def __init__(self, thing):
        '''
        Construct the `FreezerPropertyFreezer`.
        
        `thing` is the object to whom the `FreezerProperty` belongs.
        '''
        
        self.thing = thing
        '''The object to whom the `FreezerProperty` belongs.'''
        
                
    def freeze_handler(self):
        '''Call the `FreezerProperty`'s internal freeze handler.'''
        return self.freezer_property._freeze_handler(self.thing)
    
    
    def thaw_handler(self):
        '''Call the `FreezerProperty`'s internal thaw handler.'''
        return self.freezer_property._thaw_handler(self.thing)
    