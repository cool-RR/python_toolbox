# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.third_party import inspect
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict
from garlicsim.general_misc import dict_tools


#class MissionAccomplished(Exception): # tododoc: Make inaccessible
    #pass


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
        
        # The number of args which have default values:
        n_defaultful_args = len(s_defaults)
        # The word "defaultful" means "something which has a default".
        
        #######################################################################
        # Phase 1: We specify all the args that don't have a default as
        # positional args:
        defaultless_args = s_args[:-n_defaultful_args]
        self.args += dict_tools.get_list(getcallargs_result, defaultless_args)

        
        #######################################################################
        # Phase 2: We now have to deal with args that have a default. Some of
        # them, possibly none and possibly all of them, should be given
        # positionally. Some of them, possibly none, should be given by keyword.
        # And some of them, possibly none and possibly all of them, should not be
        # given at all. It is our job to figure out in which way each argument
        # should be given.
        
        # In this variable:
        n_defaultful_args_to_specify_positionally = None
        # We will put the number of defaultful arguments that should be
        # specified positionally.
        
        defaultful_args = s_args[-n_defaultful_args:]
        
        # Dict that maps from argument name to default value:
        defaults = OrderedDict(zip(defaultful_args, s_defaults))
        
        values_differing_from_defaults = OrderedDict(
            (key, value) for (key, value) in defaultful_args.iteritems()
            if value != getcallargs_result[key]
        )
        
        if s_star_args and getcallargs_result[s_star_args]:
            # We have some arguments that go into *args! This means that we
            # don't even need to think hard, we can already be sure that we're
            # going to have to specify *all* of the defaultful arguments
            # positionally, otherwise it will be impossible to put arguments in
            # *args.
            n_defaultful_args_to_specify_positionally = n_defaultful_args
            
            
        else:

            # Dict mapping from each defaultful arg to the "price" of specifying
            # its value:
            prices_of_values = OrderedDict(
                ((defaultful_arg, len(repr(getcallargs_result[defaultful_arg]))) for 
                 defaultful_arg in defaultful_args)
            )
            # The price is simply the string length of the value's repr.
            
            # Dict mapping from each defaultful arg to the "price" of specifying
            # it as a keyword (not including the length of the value):
            prices_of_keyword_prefixes = OrderedDict(
                ((defaultful_arg, len(defaultful_args)+1) for 
                 defaultful_arg in defaultful_args)
            )
            # For example, if we have a defaultful arg "gravity_strength", then
            # specifiying it by keyword will require using the string
            # "gravity_strength=", which is 17 characters long, therefore the
            # price is 17.
            
            # Now we need to decide just how many defaultful args we are going
            # to specify positionally. The options are anything from `0` to
            # `n_defaultful_args`. We're going to go one by one, and calcluate
            # the price for each candidate, and put it in this dict:
            total_price_for_n_dasp_candidate = OrderedDict()
            # (The `n_dasp` here is an abbreivation of the
            # `n_defaultful_args_to_specify_positionally` variable defined
            # before.)            
            # After we have the price for each option, we'll select the one with
            # the lowest price.
            
            for candidate in xrange(n_defaultful_args + 1):
                price = 777 todo todo todo
                # ...
                total_price_for_n_dasp_candidate[candidate] = price
                
            minimum_price = min(total_price_for_n_dasp_candidate.itervalues())
            
            leading_candidates = [
                candidate for candidate in 
                total_price_for_n_dasp_candidate.iterkeys() if
                total_price_for_n_dasp_candidate[candidate] == minimum_price
            ]
            
            if len(leading_candidates) == 1:
                # We finished with one candidate which has the minimum price.
                # This is our winner.
                (winner,) = leading_candidates
                n_defaultful_args_to_specify_positionally = winner
            
            else:
                # We have a draw! We're gonna have to settle it by
                    
        
        
        
        
        
        
        
        

        for arg_name_or_list in s_args:
            self._process_arg_name_or_list(arg_name_or_list)
                
        
    def _process_arg_name_or_list(self, arg_name_or_list, raw_args, s_defaults):
        if isinstance(arg_name_or_list, basestring):
            arg_name = arg_name_or_list
            
        else:
            assert isinstance(arg_name_or_list, list)
            