# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StepProfile` class.

See its documentation for more information.
'''

import copy

from garlicsim.general_misc import caching
from garlicsim.general_misc import cute_inspect
from garlicsim.general_misc.arguments_profile import ArgumentsProfile
from garlicsim.general_misc import address_tools
from garlicsim.misc.exceptions import GarlicSimException

import garlicsim

from garlicsim.misc.simpack_grokker.step_type import BaseStep


__all__ = ['StepProfile']


class Placeholder(object):
    '''A placeholder used instead of a state or a history browser.'''


class StepProfile(ArgumentsProfile):
    '''
    Profile for doing simulation step, specifying step function and arguments.
    
    Using different step profiles, you can crunch your simulation in different
    ways, using different world laws, different contsants and different
    algorithm, within the same project.

    The step profile contains three things:
    
      1. A reference to the step fucntion. (`.step_function`)
      2. A `tuple` of arguments. (`.args`)
      3. A `dict` of keyword arguments. (`.kwargs`)
      
    For example, if you're doing a simulation of Newtonian Mechanics, you can
    create a step profile with `kwargs` of {'G': 3.0} in order to change the
    graviational constant of the simulation on-the-fly.
    '''

    
    __metaclass__ = caching.CachedType
    
    
    def __init__(self, step_function, *args, **kwargs):
        '''
        Construct the step profile.
        
        Give the `*args` and/or `**kwargs` that you want to use for the step
        function.
        '''
        
        # Perhaps we were passed a `StepProfile` object instead of args
        # and kwargs? If so load that one, cause we're all cool and nice.
        candidate = None
        if len(args) == 1 and len(kwargs) == 0:
            candidate = args[0]
        if len(args) == 0 and len(kwargs) == 1 and \
           ('step_profile' in kwargs):
            candidate = kwargs['step_profile']
        
        if isinstance(candidate, StepProfile):
            ArgumentsProfile.__init__(self, candidate.step_function,
                                      *((Placeholder,) + candidate.args),
                                      **candidate.kwargs)
        else:
            ArgumentsProfile.__init__(self, step_function,
                                      *((Placeholder,) + args),
                                      **kwargs)

        assert self.args[0] is Placeholder
        
        self.args = self.args[1:]
        '''The `*args` that will be passed to the step function.'''
        
        self.kwargs = self.kwargs
        '''The `*kwargs` that will be passed to the step function.'''
        
        self.step_function = self.function
        '''The step function that will be used to crunch the simulation.'''
        
    
    @staticmethod
    @caching.cache()    
    def build_parser(default_step_function):
        '''
        Create a parser which builds a step profile smartly.
        
        The canonical way to build a step profile is to provide it with a step
        function, `*args` and `**kwargs`. But in the parser we're being a
        little smarter so the user will have less work.
        
        A `default_step_function` must be given, which the parser will use if
        no other step function will be given to it.
        '''
        
        def parse_arguments_to_step_profile(*args, **kwargs):
            '''
            Build a step profile smartly.
        
            The canonical way to build a step profile is to provide it with a
            step function, `*args` and `**kwargs`. But in this function we're
            being a little smarter so the user will have less work.
            
            You do not need to enter a step function; we will use the default
            one, unless you specify a different one as `step_function`.
            
            You may also pass in a step profile as `step_profile`, and it will
            be noticed and used.
            '''
        
            # We have two candidates to check now: `args[0]` and
            # `kwargs['step_function']`. We'll check the latter first, because
            # that's more explicit and there's less chance we'll be catching
            # some other object by mistake.
            #
            # So we start with `kwargs`:
            
            if 'step_function' in kwargs:
                kwargs_copy = kwargs.copy()
                step_function = kwargs_copy.pop('step_function')
                
                
                assert BaseStep.__instancecheck__(step_function)
                # If the user specified 'step_function', he's not going to get
                # away with it not being an actual step function.
    
                return StepProfile(step_function, *args, **kwargs_copy)
            
            
            if 'step_profile' in kwargs:
                kwargs_copy = kwargs.copy()
                step_profile = kwargs_copy.pop('step_profile')
                
                if step_profile is None:
                    # We let the user specify `step_profile=None` if he wants
                    # to get the default step profile.
                    return StepProfile(default_step_function)
                    
                else: # step_profile is not None
                    if not isinstance(step_profile, StepProfile):
                        raise GarlicSimException(
                            "You passed in `%s` as a keyword argument with a "
                            "keyword of `step_profile`, but it's not a step "
                            "profile." % step_profile
                        )
                    return step_profile
    
            
            # No step function in `kwargs`. We'll try `args`:
            
            elif args:
                
                candidate = args[0]
                
                if isinstance(candidate, StepProfile):
                    return candidate
                
                elif BaseStep.__instancecheck__(candidate):
                    args_copy = args[1:]
                    return StepProfile(
                        candidate,
                        *args_copy,
                        **kwargs
                    )
                  
            
            
            return StepProfile(default_step_function, *args, **kwargs)
        
        return parse_arguments_to_step_profile
                
    
    def __repr__(self, short_form=False, root=None, namespace={}):
        '''
        Get a string representation of the step profile.
        
        Example output with `short_form=False`:
        
            StepProfile(<unbound method State.step>, 'billinear', t=7)
            
        Use `short_form=True` for the shorter form:
        
            my_simpack.State.step(<state>, 'billinear', t=7)
            
        `root` and `namespace` will be used for shortening the function
        address.
        '''
        
        if short_form:
            
            if root is None:
                # Let's try to guess the simpack to have a shorter result:
                root = self._guess_simpack()
                # (When `_guess_simpack` fails, it returns `None`, so we're
                # safe.)
                    
            describe = lambda thing: address_tools.describe(
                thing,
                shorten=True,
                root=root,
                namespace=namespace
            )
        else: # not short_form
            describe = repr

        args_string = ', '.join((describe(thing) for thing in self.args))
        kwargs_string = ', '.join(
            ('='.join((str(key), describe(value))) for
            (key, value) in self.kwargs.iteritems())
        )
        strings = filter(None, (args_string, kwargs_string))
        big_string = ', '.join(strings)
        
            
        if short_form:
            step_function_address = describe(self.step_function)
            final_big_string = ', '.join(
                filter(
                    None,
                    (
                        '<state>',
                        big_string
                    )
                )
            )
            return '%s(%s)' % (
                step_function_address,
                final_big_string
            )
            
        else:
            final_big_string = ', '.join(
                filter(
                    None,
                    (
                        describe(self.step_function),
                        big_string
                    )
                )
            )
            return '%s(%s)' % (type(self).__name__, final_big_string)
    

    @classmethod
    def create_from_dld_format(cls, step_function, args_dict, star_args_list,
                               star_kwargs_dict):
        '''
        Create a step profile from data given in the "dict-list-dict" format.
        
        The "dict-list-dict" format means that in addition to a step function,
        we get a `dict` of arguments, a `list` of `*args`, and a `dict` of
        `**kwargs`.
        '''
        args_spec = cute_inspect.getargspec(step_function)
        new_args = [args_dict[name] for name in args_spec.args[1:]] + \
                   list(star_args_list)
        return cls(step_function, *new_args, **star_kwargs_dict)
        
    
    def _guess_simpack(self):
        '''`try` to guess the simpack that this step profile belongs to.'''
        try:
            module = \
                address_tools.resolve(self.step_function.__module__)
        except Exception:
            return None
        else:
            if hasattr(module, 'State'):
                if issubclass(module.State, garlicsim.data_structures.State):
                    return garlicsim.misc.simpack_tools.getting_from_state.\
                           get_from_state_class(module.State)
                
                           
    def __eq__(self, other):
        return isinstance(other, StepProfile) and \
               ArgumentsProfile.__eq__(self, other)

    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    