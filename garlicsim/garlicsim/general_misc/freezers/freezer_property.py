# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

from garlicsim.general_misc import caching
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc.misc_tools import do_nothing

from .freezer import Freezer


class FreezerProperty(caching.CachedProperty):
    ''' '''
    #blocktodo: doc argument
    def __init__(self, on_freeze=do_nothing, on_thaw=do_nothing,
                 freezer_type=Freezer, doc=None, name=None):
        if freezer_type is not Freezer:
            # blocktodo: helpful exception, also in decorators
            assert on_freeze is on_thaw is do_nothing
            
        self.__freezer_type = freezer_type
        self._freeze_handler = on_freeze
        self._thaw_handler = on_thaw
        caching.CachedProperty.__init__(self,
                                        getter=self.__make_freezer,
                                        doc=doc,
                                        name=name)
        
    def __make_freezer(self, obj):
        assert obj is not None
        
        freezer = self.__freezer_type(obj)
        freezer._Freezer__freezer_property = self
        return freezer
            
        
    def on_freeze(self, function):
        self._freeze_handler = function
        return function

        
    def on_thaw(self, function):
        self._thaw_handler = function
        return function
        

        