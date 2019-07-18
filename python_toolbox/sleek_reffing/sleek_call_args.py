# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `SleekCallArgs` class.

See its documentation for more details.
'''

import inspect

from python_toolbox import cheat_hashing

from .sleek_ref import SleekRef
from .cute_sleek_value_dict import CuteSleekValueDict


__all__ = ['SleekCallArgs']


class SleekCallArgs:
    '''
    A bunch of call args with a sleekref to them.

    "Call args" is a mapping of which function arguments get which values.
    For example, for a function:

        def f(a, b=2):
            pass

    The calls `f(1)`, `f(1, 2)` and `f(b=2, a=1)` all share the same call args.

    All the argument values are sleekreffed to avoid memory leaks. (See
    documentation of `python_toolbox.sleek_reffing.SleekRef` for more details.)
    '''
    # What if we one of the args gets gc'ed before this SCA gets added to the
    # dictionary? It will render this SCA invalid, but we'll still be in the
    # dict. So make note to user: Always keep reference to args and kwargs
    # until the SCA gets added to the dict.
    def __init__(self, containing_dict, function, *args, **kwargs):
        '''
        Construct the `SleekCallArgs`.

        `containing_dict` is the `dict` we'll try to remove ourselves from when
        one of our sleekrefs dies. `function` is the function for which we
        calculate call args from `*args` and `**kwargs`.
        '''

        self.containing_dict = containing_dict
        '''
        `dict` we'll try to remove ourselves from when 1 of our sleekrefs dies.
        '''

        args_spec = inspect.getfullargspec(function)
        star_args_name, star_kwargs_name = args_spec.varargs, args_spec.varkw

        call_args = inspect.getcallargs(function, *args, **kwargs)
        del args, kwargs

        self.star_args_refs = []
        '''Sleekrefs to star-args.'''

        if star_args_name:
            star_args = call_args.pop(star_args_name, None)
            if star_args:
                self.star_args_refs = [SleekRef(star_arg, self.destroy) for
                                       star_arg in star_args]

        self.star_kwargs_refs = {}
        '''Sleerefs to star-kwargs.'''
        if star_kwargs_name:
            star_kwargs = call_args.pop(star_kwargs_name, {})
            if star_kwargs:
                self.star_kwargs_refs = CuteSleekValueDict(self.destroy,
                                                           star_kwargs)

        self.args_refs = CuteSleekValueDict(self.destroy, call_args)
        '''Mapping from argument name to value, sleek-style.'''

        # In the future the `.args`, `.star_args` and `.star_kwargs` attributes
        # may change, so we must record the hash now:
        self._hash = cheat_hashing.cheat_hash(
            (
                self.args,
                self.star_args,
                self.star_kwargs
            )
        )



    args = property(lambda self: dict(self.args_refs))
    '''The arguments.'''

    star_args = property(
        lambda self:
            tuple((star_arg_ref() for star_arg_ref in self.star_args_refs))
    )
    '''Extraneous arguments. (i.e. `*args`.)'''

    star_kwargs = property(lambda self: dict(self.star_kwargs_refs))
    '''Extraneous keyword arguments. (i.e. `*kwargs`.)'''


    def destroy(self, _=None):
        '''Delete ourselves from our containing `dict`.'''
        if self.containing_dict:
            try:
                del self.containing_dict[self]
            except KeyError:
                pass


    def __hash__(self):
        return self._hash


    def __eq__(self, other):
        if not isinstance(other, SleekCallArgs):
            return NotImplemented
        return self.args == other.args and \
               self.star_args == other.star_args and \
               self.star_kwargs == other.star_kwargs


    def __ne__(self, other):
        return not self == other


