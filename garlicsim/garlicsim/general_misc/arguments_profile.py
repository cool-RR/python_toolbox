# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.third_party import inspect
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict
from garlicsim.general_misc import dict_tools

# Canonical: As few characters as possible, and after that as many keyword
# arguments as possible.

class ArgumentsProfile(object):
    def __init__(self, function, *args, **kwargs):
        self.function = function
        raw_args = args
        raw_kwargs = kwargs
        del args, kwargs
        
        self.args = []
        self.kwargs = OrderedDict()
        
        args_spec = inspect.getargspec(function)
        
        (s_args, s_star_args, s_star_kwargs, s_defaults) = args_spec
        
        getcallargs_result = inspect.getcallargs(function,
                                                 self._raw_args,
                                                 self._raw_kwargs)
        
        
        #######################################################################
        # Phase 1: We specify all the args that don't have a default as
        # positional args:
        defaultless_args = s_args[:-len(s_defaults)]
        self.args += dict_tools.get_list(getcallargs_result, defaultless_args)

        
        #######################################################################
        # Phase 2: ???
        
        # Creating a dict that maps from argument name to default value:
        args_with_defaults = OrderedDict(
            zip(s_args[-len(s_defaults):], s_defaults)
        )
        
        args_differing_from_defaults = OrderedDict(
            (key, value) for (key, value) in args_with_defaults.iteritems()
            if value != getcallargs_result[key]
        )
        

        for arg_name_or_list in s_args:
            self._process_arg_name_or_list(arg_name_or_list)
                
        
    def _process_arg_name_or_list(self, arg_name_or_list, raw_args, s_defaults):
        if isinstance(arg_name_or_list, basestring):
            arg_name = arg_name_or_list
            
        else:
            assert isinstance(arg_name_or_list, list)
            