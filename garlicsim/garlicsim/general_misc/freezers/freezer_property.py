# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

from garlicsim.general_misc import caching
from garlicsim.general_misc.misc_tools import do_nothing

from .freezer import Freezer


class FreezerProperty(caching.CachedProperty):
    ''' '''
    #blocktodo: doc argument
    def __init__(self, on_freeze=do_nothing, on_thaw=do_nothing,
                 freezer_type=Freezer, doc=None):
        self.__our_name = None
        if freezer_type is not Freezer:
            # blocktodo: helpful exception, also in decorators
            assert on_freeze is on_thaw is do_nothing
        self.__freezer_type = freezer_type
        self._freeze_handler = on_freeze
        self._thaw_handler = on_thaw
        caching.CachedProperty.__init__(self,
                                        getter=self.__make_freezer,
                                        doc=doc)
        
    def __make_freezer(self, obj):
        assert obj is not None
        
        freezer = self.__freezer_type(obj)
        freezer._Freezer__freezer_property = self
        return freezer
        #freezer.reentrant_enter = \
            #lambda: self.__freeze_handler(obj)
        #freezer.reentrant_exit = \
            #lambda type_, value, traceback: self.__thaw_handler(obj)
            
        
    def on_freeze(self, function):
        self._freeze_handler = function
        return function

        
    def on_thaw(self, function):
        self._thaw_handler = function
        return function
        

        