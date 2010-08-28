# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.third_party import inspect
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict


class ArgumentsProfile(object):
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self._raw_args = args
        self._raw_kwargs = kwargs
        
        self.args = []
        self.kwargs = OrderedDict()
        
        args_spec = inspect.getargspec(function)
        
        (self._s_args, self._s_star_args,
         self._s_star_kwargs, self._s_defaults) = args_spec
        
        self._s_defaultless_args = self._s_args[:-len(self._s_defaults)]

        for arg_name_or_list in s_args:
            self._process_arg_name_or_list(arg_name_or_list)
                
        
    def _process_arg_name_or_list(self, arg_name_or_list, raw_args, s_defaults):
        if isinstance(arg_name_or_list, basestring):
            arg_name = arg_name_or_list
            
        else:
            assert isinstance(arg_name_or_list, list)
            