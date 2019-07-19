# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing for `python_toolbox.introspection_tools.get_default_args_dict`.'''

from __future__ import generator_stop

from python_toolbox.introspection_tools import get_default_args_dict
from python_toolbox.nifty_collections import OrderedDict


def test():
    '''Test the basic workings of `get_default_args_dict`.'''
    def f(a, b, c=3, d=4):
        pass

    assert get_default_args_dict(f) == \
        OrderedDict((('c', 3), ('d', 4)))


def test_generator():
    '''Test `get_default_args_dict` on a generator function.'''
    def f(a, meow='frr', d={}):
        yield None

    assert get_default_args_dict(f) == \
        OrderedDict((('meow', 'frr'), ('d', {})))


def test_empty():
    '''Test `get_default_args_dict` on a function with no defaultful args.'''
    def f(a, b, c, *args, **kwargs):
        pass

    assert get_default_args_dict(f) == \
        OrderedDict()
