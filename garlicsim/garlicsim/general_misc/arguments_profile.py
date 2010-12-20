# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ArgumentsProfile` class.

See its documentation for more details.
'''

from garlicsim.general_misc import cute_inspect
from garlicsim.general_misc import cheat_hashing
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import cmp_tools


# Our grand definition of canonical: As few characters as possible, and after
# that as many keyword arguments as possible, with extraneous keyword arguments
# ordered alphabetically (with "_" as the highest character, so anything
# starting with "_" will be at the end.)

class ArgumentsProfile(object):
    '''
    A canonical arguments profile for a function.
    
    (This should be used only on function that don't modify the arguments they
    receive. Also, you should never modify any arguments you use in an
    arguments profile, even outside the function.)
    
    What is an arguments profile and what is it good for?
    
    It's possible to call the same function with the same arguments in
    different ways. For example, take this function:

        def f(a, bb=2, ccc=3, **kwargs):
            return (a, bb, ccc)
            
    You can call it like `f(1)` or `f(a=1)` or `f(1, ccc=3, bb=2, **{})` or
    many other different ways which will result in exactly the same arguments.
    
    To organize the different ways a function can be called, an arguments
    profile provides a canonical way to call the function, so all the different
    examples in the last paragraphs would be reduced to the same canonical
    arguments profile. (In this case `f(1)`.)
    
    The canonical arguments profile is defined as the one which satisfies the
    following criteria, with the first one being the most important, the second
    one being a tie-breaker to the first, and the third one being a tie-breaker
    to the second:
    
     1. It has as few characters as possible. (e.g. `f(1)` is better than    
        `f(1, 2)`.)
        
     2. It has as many keyword arguments as possible. (e.g. `f(bb=3)` is
        better than `f(1, 3)`.)
        
     3. The extraneous keywords (i.e. `**kwargs`) are sorted alphabetically, 
        with "_" being the highest/last character. (e.g. `f(1, cat=7, meow=7,
        _house=7)` is better than `f(1, _house=7, meow=7, cat=7)`)
    
    '''
    
    def __init__(self, function, *args, **kwargs):
        '''
        Construct the arguments profile.
        
        `*args` and `**kwargs` are the arguments that go into the `function`.
        '''
        
        if not callable(function):
            raise Exception('%s is not a callable object.' % function)
        self.function = function
        
        raw_args = args
        raw_kwargs = kwargs
        del args, kwargs
        
        self.args = ()
        self.kwargs = OrderedDict()
        
        args_spec = cute_inspect.getargspec(function)
        
        (s_args, s_star_args, s_star_kwargs, s_defaults) = args_spec
        
        # `getargspec` has a weird policy, when inspecting a function with no
        # defaults, to give a `defaults` of `None` instead of the more
        # consistent `()`. We fix that here:
        if s_defaults is None:
            s_defaults = ()
        
        getcallargs_result = cute_inspect.getcallargs(function,
                                                      *raw_args,
                                                      **raw_kwargs)
        
        self.getcallargs_result = getcallargs_result # todo: rename?
        
        # The number of args which have default values:
        n_defaultful_args = len(s_defaults)
        # The word "defaultful" means "something which has a default."
        
        
        #######################################################################
        # Phase 1: We specify all the args that don't have a default as
        # positional args:
        defaultless_args = s_args[:-n_defaultful_args] if n_defaultful_args \
                           else s_args[:]
        self.args += tuple(
            dict_tools.get_list(getcallargs_result, defaultless_args)
        )

        
        #######################################################################
        # Phase 2: We now have to deal with args that have a default. Some of
        # them, possibly none and possibly all of them, should be given
        # positionally. Some of them, possibly none, should be given by
        # keyword. And some of them, possibly none and possibly all of them,
        # should not be given at all. It is our job to figure out in which way
        # each argument should be given.
        
        # In this variable:
        n_defaultful_args_to_specify_positionally = None
        # We will put the number of defaultful arguments that should be
        # specified positionally.
        
        defaultful_args = s_args[-n_defaultful_args:] if n_defaultful_args \
                          else []
        
        # `dict` that maps from argument name to default value:
        defaults = OrderedDict(zip(defaultful_args, s_defaults))
        
        defaultful_args_differing_from_defaults = set((
            defaultful_arg for defaultful_arg in defaultful_args
            if defaults[defaultful_arg] != getcallargs_result[defaultful_arg]
        ))
        
        if s_star_args and getcallargs_result[s_star_args]:
            # We have some arguments that go into `*args`! This means that we
            # don't even need to think hard, we can already be sure that we're
            # going to have to specify *all* of the defaultful arguments
            # positionally, otherwise it will be impossible to put arguments in
            # `*args`.
            n_defaultful_args_to_specify_positionally = n_defaultful_args
            
            
        else:

            # `dict` mapping from each defaultful arg to the "price" of
            # specifying its value:
            prices_of_values = OrderedDict((
                (defaultful_arg, len(repr(getcallargs_result[defaultful_arg])))
                 for defaultful_arg in defaultful_args
            ))
            # The price is simply the string length of the value's `repr`.
            
            # `dict` mapping from each defaultful arg to the "price" of
            # specifying it as a keyword (not including the length of the
            # value):
            prices_of_keyword_prefixes = OrderedDict(
                ((defaultful_arg, len(defaultful_arg)+1) for 
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
            #
            # After we have the price for each option, we'll select the one
            # with the lowest price.
            
            # One thing to do before iterating on the candidates is to find out
            # whether the "lonely comma discount" is in effect.
            #
            # The "lonely comma discount" is given when there's nothing but
            # defaultful arguments to this function, and therefore the number
            # of ", " strings needed here is not `candidate`, but `candidate -
            # 1`, unless of course candidate is zero.
            
            if not defaultless_args and \
                (not s_star_args or not getcallargs_result[s_star_args]) and \
                (not s_star_kwargs or not getcallargs_result[s_star_kwargs]):
                
                lonely_comma_discount_may_be_given = True
            
            else:
                
                lonely_comma_discount_may_be_given = False
            
            # Now we iterate on the candidates to find out which one has the
            # lowest price:
            
            for candidate in xrange(n_defaultful_args + 1):

                defaultful_args_to_specify_positionally = \
                    defaultful_args[:candidate]
                
                price_for_positionally_specified_defaultful_args = \
                    2 * candidate + \
                    sum(
                        dict_tools.get_list(
                            prices_of_values,
                            defaultful_args_to_specify_positionally
                        )
                    )
                # The `2 * candidate` addend is to account for the ", " parts
                # between the arguments.
                    
                defaultful_args_to_specify_by_keyword = filter(
                    defaultful_args_differing_from_defaults.__contains__,
                    defaultful_args[candidate:]
                )
                
                price_for_defaultful_args_specified_by_keyword = \
                    2 * len(defaultful_args_to_specify_by_keyword) + \
                    sum(
                        dict_tools.get_list(
                            prices_of_keyword_prefixes,
                            defaultful_args_to_specify_by_keyword
                        )
                    ) + \
                    sum(
                        dict_tools.get_list(
                            prices_of_values,
                            defaultful_args_to_specify_by_keyword
                        )
                    )
                # The `2 * len(...)` addend is to account for the ", " parts
                # between the arguments.
                
                # Now we need to figure out if this candidate gets the "lonely
                # comma discount".
                if lonely_comma_discount_may_be_given and \
                   (defaultful_args_to_specify_by_keyword or \
                    defaultful_args_to_specify_positionally):
                    
                    lonely_comma_discount = -2
                    
                else:
                    lonely_comma_discount = 0
                
                price = price_for_positionally_specified_defaultful_args + \
                        price_for_defaultful_args_specified_by_keyword + \
                        lonely_comma_discount
                
                total_price_for_n_dasp_candidate[candidate] = price


            # Finished iterating on candidates! Time to pick our winner.
                
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
                # We have a draw! We're gonna have to settle it by picking the
                # lowest candidate, because in our definition of "canonical
                # arguments profile", our second priority after "as few
                # characters as possible" is "as many keyword arguments as
                # possible".
                winner = leading_candidates[0]
                
            n_defaultful_args_to_specify_positionally = winner
            
        # We have a winner! Now we know exactly which defaultful args should
        # be specified positionally and which should be specified by
        # keyword.
            
        # First we add the positionally specified:
            
        defaultful_args_to_specify_positionally = \
            defaultful_args[:n_defaultful_args_to_specify_positionally]
        self.args += tuple(
            (getcallargs_result[defaultful_arg] for defaultful_arg
             in defaultful_args_to_specify_positionally)
        )
        
        # Now we add those specified by keyword:

        defaultful_args_to_specify_by_keyword = filter(
                defaultful_args_differing_from_defaults.__contains__,
                defaultful_args[n_defaultful_args_to_specify_positionally:]
            )
        for defaultful_arg in defaultful_args_to_specify_by_keyword:
            self.kwargs[defaultful_arg] = getcallargs_result[defaultful_arg]
                
        
        #######################################################################
        # Phase 3: Add the star args:
        
        if s_star_args and getcallargs_result[s_star_args]:
            
            assert not self.kwargs
            # Just making sure that no non-star args were specified by keyword,
            # which would make it impossible for us to put stuff in `*args`.
            
            self.args += getcallargs_result[s_star_args]        

            
        #######################################################################
        # Phase 4: Add the star kwargs:
        
        if s_star_kwargs and getcallargs_result[s_star_kwargs]:
            
            # We can't just add the `**kwargs` as is; We need to add them
            # according to canonical ordering. So we need to sort them first.
            
            unsorted_star_kwargs_names = \
                getcallargs_result[s_star_kwargs].keys()
            sorted_star_kwargs_names = sorted(
                unsorted_star_kwargs_names,
                cmp=cmp_tools.underscore_hating_cmp
            )
            
            sorted_star_kwargs = OrderedDict(
                zip(
                    sorted_star_kwargs_names,
                    dict_tools.get_list(
                        getcallargs_result[s_star_kwargs],
                        sorted_star_kwargs_names
                    )
                )
            )
            
            
            self.kwargs.update(sorted_star_kwargs)
            
        # All phases completed! This arguments profile is canonical and ready.
        #######################################################################
        
        # Caching the hash, since its computation can take a long time:
        self._hash = cheat_hashing.cheat_hash(
            (
                self.function,
                self.args,
                tuple(self.kwargs)
            )
        )
        
    
    @classmethod
    def create_from_dld_format(cls, function, args_dict, star_args_list,
                               star_kwargs_dict):
        '''
        Create an arguments profile from data given in "dict-list-dict" format.
        
        The "dict-list-dict" format means that in addition to a function, we
        get a `dict` of arguments, a `list` of `*args`, and a `dict` of
        `**kwargs`.
        '''
        args_spec = cute_inspect.getargspec(function)
        new_args = [args_dict[name] for name in args_spec.args] + \
                   list(star_args_list)
        return cls(function, *new_args, **star_kwargs_dict)
        
            
                    
    def __eq__(self, other):
        # todo: maybe raise warning when unbound method is compared with same
        # method just bound with the object passed to the unbound method, and
        # the result of both functions would be the same, but we're not smart
        # enough to say it's the same arguments profile, so raise a warning.
        if not isinstance(other, ArgumentsProfile):
            return NotImplemented
        # Note that we're comparing the functions with a `==` here. This lesson
        # cost me a couple of days: `MyClass.method == MyClass.method` but
        # `MyClass.method is not MyClass.method`.
        return (self.function == other.function) and \
               (self.args == other.args) and \
               (self.kwargs == other.kwargs)
    
    
    def __hash__(self):
        return self._hash
                    

    
    