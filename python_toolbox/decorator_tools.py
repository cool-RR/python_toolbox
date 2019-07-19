# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Tools for decorators.'''

import functools
import inspect
import types

from python_toolbox.third_party import decorator as michele_decorator_module


def helpful_decorator_builder(decorator_builder):
    '''
    Take a decorator builder and return a "helpful" version of it.

    A decorator builder is a function that returns a decorator. A decorator
    is used like this:

        @foo
        def bar():
            pass

    While a decorator *builder* is used like this

        @foo()
        def bar():
            pass

    The parentheses are the difference.

    Sometimes the user forgets to put parentheses after the decorator builder;
    in that case, a helpful decorator builder is one that raises a helpful
    exception, instead of an obscure one. Decorate your decorator builders with
    `helpful_decorator_builder` to make them raise a helpful exception when the
    user forgets the parentheses.

    Limitations:

      - Do not use this on decorators that may take a function object as their
        first argument.

      - Cannot be used on classes.

    '''

    assert isinstance(decorator_builder, types.FunctionType)

    def inner(*args, **kwargs):

        if args and isinstance(args[0], types.FunctionType):
            function = args[0]
            function_name = function.__name__
            decorator_builder_name = decorator_builder.__name__
            raise TypeError(
                f'It seems that you forgot to add parentheses after '
                f'@{decorator_builder_name} when decorating the '
                f'{function_name} function.'
            )
        else:
            return decorator_builder(*args, **kwargs)

    return functools.wraps(decorator_builder)(inner)
