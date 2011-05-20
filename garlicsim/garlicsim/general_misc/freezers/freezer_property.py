# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

from garlicsim.general_misc import caching
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc.misc_tools import do_nothing

from .freezer_property_freezer import FreezerPropertyFreezer


class FreezerProperty(caching.CachedProperty):
    ''' '''
    def __init__(self, on_freeze=do_nothing, on_thaw=do_nothing,
                 freezer_type=FreezerPropertyFreezer, doc=None, name=None):
        
        if freezer_type is not FreezerPropertyFreezer:
            if not (on_freeze is on_thaw is do_nothing):
                raise Exception(
                    "You've passed a `freezer_type` argument, so you're not "
                    "allowed to pass `on_freeze` or `on_thaw` arguments. The "
                    "freeze/thaw handlers should be defined on the freezer "
                    "type."
                )
            
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
        freezer.freezer_property = self
        return freezer
            
        
    def on_freeze(self, function):
        if self.__freezer_type is not FreezerPropertyFreezer:
            raise Exception(
                "You've passed a `freezer_type` argument, so you're not "
                "allowed to use the `on_freeze` or `on_thaw` decorators. The "
                "freeze/thaw handlers should be defined on the freezer "
                "type."
            )
        self._freeze_handler = function
        return function

        
    def on_thaw(self, function):
        if self.__freezer_type is not FreezerPropertyFreezer:
            raise Exception(
                "You've passed a `freezer_type` argument, so you're not "
                "allowed to use the `on_freeze` or `on_thaw` decorators. The "
                "freeze/thaw handlers should be defined on the freezer "
                "type."
            )
        self._thaw_handler = function
        return function
        

        