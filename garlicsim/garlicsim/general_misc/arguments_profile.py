# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.third_party import inspect
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict
from garlicsim.general_misc import dict_tools


#class MissionAccomplished(Exception): # tododoc: Make inaccessible
    #pass


# Our grand definition of canonical: As few characters as possible, and after
# that as many keyword arguments as possible, with extraneous keyword arguments
# ordered alphabetically (with "_" as the highest character, so anything
# starting with "_" will be at the end.)

class ArgumentsProfile(object):
    '''
    Note this should be used only on functions that don't modify argmunets
    '''
    
    def __init__(self, function, *args, **kwargs):
        self.function = function
        raw_args = args
        raw_kwargs = kwargs
        del args, kwargs
        
        self.args = ()
        self.kwargs = OrderedDict()
        
        args_spec = inspect.getargspec(function)
        
        (s_args, s_star_args, s_star_kwargs, s_defaults) = args_spec
        
        # `getargspec` has a weird policy, when inspecting a function with no
        # defaults, to give a `defaults` of `None` instead of the more
        # consistent `()`. We fix that here:
        if s_defaults is None:
            s_defaults = ()
        
        getcallargs_result = inspect.getcallargs(function,
                                                 *raw_args,
                                                 **raw_kwargs)
        
        # The number of args which have default values:
        n_defaultful_args = len(s_defaults)
        # The word "defaultful" means "something which has a default".
        
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
        # positionally. Some of them, possibly none, should be given by keyword.
        # And some of them, possibly none and possibly all of them, should not be
        # given at all. It is our job to figure out in which way each argument
        # should be given.
        
        # In this variable:
        n_defaultful_args_to_specify_positionally = None
        # We will put the number of defaultful arguments that should be
        # specified positionally.
        
        defaultful_args = s_args[-n_defaultful_args:] if n_defaultful_args \
                          else []
        
        # Dict that maps from argument name to default value:
        defaults = OrderedDict(zip(defaultful_args, s_defaults))
        
        defaultful_args_differing_from_defaults = set((
            defaultful_arg for defaultful_arg in defaultful_args
            if defaults[defaultful_arg] != getcallargs_result[defaultful_arg]
        ))
        
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
            # After we have the price for each option, we'll select the one with
            # the lowest price.
            
            # One thing to do before iterating on the candidates is to find out
            # whether the "lonely comma discount" is in effect.
            # The "lonely comma discount" is given when there's nothing but
            # defaultful arguments to this function, and therefore the number of
            # ", " strings needed here is not `candidate`, but `candidate - 1`,
            # unless of course candidate is zero.
            
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
                # The `2 * candidate` part is to account for the ", " parts
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
                # The `2 * len(...)` part is to account for the ", " parts
                # between the arguments.
                
                # Now we need to figure out if this candidate gets the "lonely
                # comma discount".
                if lonely_comma_discount_may_be_given and candidate > 0:
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
        self.args += tuple((getcallargs_result[defaultful_arg] for defaultful_arg
                      in defaultful_args_to_specify_positionally))
        
        # Now we add those specified by keyword:

        defaultful_args_to_specify_by_keyword = filter(
                defaultful_args_differing_from_defaults.__contains__,
                defaultful_args[n_defaultful_args_to_specify_positionally:]
            )
        for defaultful_arg in defaultful_args_to_specify_by_keyword:
            self.kwargs[defaultful_arg] = getcallargs_result[defaultful_arg]
                
        #######################################################################
        # Phase 3: ???
            
    def __eq__(self, other):
        if not isinstance(other, ArgumentsProfile):
            raise Exception
        return (self.function is other.function) and \
               (self.args == other.args) and \
               (self.kwargs == other.kwargs)
    
            
                    
        
        
if __name__ == '__main__':
    
    def f(a, b, c):
        pass
    
    a1 = ArgumentsProfile(f, 1, 2, 3)
    assert a1.args == (1, 2, 3)
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(f, 1, c=3, b=2)
    a3 = ArgumentsProfile(f, c=3, a=1, b=2)
    a4 = ArgumentsProfile(f, 1, **{'c': 3, 'b': 2})
    a5 = ArgumentsProfile(f, **OrderedDict((('c', 3), ('b',  2), ('a',  1))))
    assert a1 == a2 == a3 == a4 == a5
    
    
    
    def g(a, b, c='three', d='four'):
        pass
    
    a1 = ArgumentsProfile(g, 'one', 'two')
    assert a1.args == ('one', 'two')
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(g, 'one', 'two', 'three')
    a3 = ArgumentsProfile(g, 'one', 'two', 'three', 'four')
    assert a1 == a2 == a3
    
    a4 = ArgumentsProfile(g, 'one', 'two', 'dynamite')
    assert a1 != a4
    assert a4.args == ('one', 'two', 'dynamite')
    assert not a4.kwargs
    
    a5 = ArgumentsProfile(g, 'one', 'two', c='dynamite')
    a6 = ArgumentsProfile(g, 'one', 'two', 'dynamite', 'four')
    a7 = ArgumentsProfile(g, 'one', 'two', c='dynamite', d='four')
    a8 = ArgumentsProfile(g, 'one', 'two', 'dynamite', d='four')
    a9 = ArgumentsProfile(g, a='one', b='two', c='dynamite', d='four')
    a10 = ArgumentsProfile(g, d='four', c='dynamite', b='two', a='one')
    a11 = ArgumentsProfile(g, 'one', c='dynamite', d='four', b='two')
    assert a4 == a5 == a6 == a7 == a8 == a9 == a10 == a11
    
    a12 = ArgumentsProfile(g, 'one', 'two', d='bang')
    assert a12.args == ('one', 'two')
    assert a12.kwargs == OrderedDict((('d', 'bang'),))
    
    a13 = ArgumentsProfile(g, 'one', 'two', 'three', d='bang')
    a14 = ArgumentsProfile(g, 'one', 'two', c='three', d='bang')
    a15 = ArgumentsProfile(g, 'one', 'two', 'three', 'bang')
    a16 = ArgumentsProfile(g, a='one', b='two', c='three', d='bang')
    a17 = ArgumentsProfile(g, b='two', c='three', d='bang', a='one')
    assert a13 == a14 == a15 == a16 == a17
    
    
    
    def h(a, b, creativity=3, d=4):
        pass
    
    a1 = ArgumentsProfile(h, 1, 2)
    assert a1.args == (1, 2)
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(h, 1, 2, 3, 4)
    a3 = ArgumentsProfile(h, a=1, b=2, creativity=3, d=4)
    a4 = ArgumentsProfile(h, creativity=3, d=4, a=1, b=2)
    a5 = ArgumentsProfile(h, 1, 2, creativity=3, d=4)
    assert a1 == a2 == a3 == a4 == a5
    
    a6 = ArgumentsProfile(h, 1, 2, d='booyeah')
    assert a6.args == (1, 2)
    assert a6.kwargs == OrderedDict((('d', 'booyeah'),))
    
    a7 = ArgumentsProfile(h, 1, 2, 3, 'booyeah')
    a8 = ArgumentsProfile(h, 1, 2, creativity=3, d='booyeah')
    assert a6 == a7 == a8
    
    
    
    def f(a, b, c=3, dragon=4):
        pass
    
    a1 = ArgumentsProfile(f, 1, 2)
    assert a1.args == (1, 2)
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(f, 1, 2, 3, 4)
    a3 = ArgumentsProfile(f, a=1, b=2, c=3, dragon=4)
    a4 = ArgumentsProfile(f, c=3, dragon=4, a=1, b=2)
    a5 = ArgumentsProfile(f, 1, 2, c=3, dragon=4)
    assert a1 == a2 == a3 == a4 == a5
    
    a6 = ArgumentsProfile(f, 1, 2, dragon='booyeah')
    assert a6.args == (1, 2, 3, 'booyeah')
    assert not a6.kwargs
    
    a7 = ArgumentsProfile(f, 1, 2, 3, 'booyeah')
    a8 = ArgumentsProfile(f, 1, 2, c=3, dragon='booyeah')
    assert a6 == a7 == a8
    
    
    
    def func(a, b, c=3, dragon=4, e=5, f=6, glide=7, human=8):
        pass
        
    a1 = ArgumentsProfile(func, 1, 2, glide='boom')
    assert a1.args == (1, 2)
    assert a1.kwargs == OrderedDict((('glide', 'boom'),))
    
    a2 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom')
    a3 = ArgumentsProfile(func, 1, 2, 3, glide='boom')
    assert a1 == a2 == a3
    
    a4 = ArgumentsProfile(func, 1, 2, glide='boom', human='pow')
    a5 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom', 'pow')
    # edge case, second priority
    assert a4.args == (1, 2)
    assert a4.kwargs == OrderedDict((('glide', 'boom'), ('human', 'pow')))
    assert a4 == a5
    
    
    
    def func(a, b, c=3, dragon=4, e=5, f=6, glide=7, human=8, iris=9):
        pass
        
    a1 = ArgumentsProfile(func, 1, 2, glide='boom')
    assert a1.args == (1, 2)
    assert a1.kwargs == OrderedDict((('glide', 'boom'),))
    
    a2 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom')
    a3 = ArgumentsProfile(func, 1, 2, 3, glide='boom')
    assert a1 == a2 == a3
    
    a4 = ArgumentsProfile(func, 1, 2, glide='boom', human='pow', iris='badabang')
    a5 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom', 'pow', 'badabang')
    assert a4 == a5
    assert a4.args == (1, 2, 3, 4, 5, 6, 'boom', 'pow', 'badabang')
    assert not a4.kwargs
    
    
    
    
    
    
    
    
    #assert False
