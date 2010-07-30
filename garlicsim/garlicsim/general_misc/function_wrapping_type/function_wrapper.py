# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


import types

from garlicsim.general_misc import misc_tools

class FunctionWrapper(object):
    def __init__(self, function=None, function_address=None):
        assert function or function_address
        if function:
            assert isinstance(function, types.FunctionType)
        assert function_address is not None, 'Not implemented yet, tododoc'
        self.function = function or misc_tools.get_object_from_address(function_address)
        self.function_address = function_address
        self.__call__ = function.__call__
    
    def __getstate__(self):
        return self.function_address
    
    def __setstate__(self, function_address):
        self.__init__(function_address=function_address)
    
    
        
    