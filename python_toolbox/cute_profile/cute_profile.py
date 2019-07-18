# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `profile_ready` decorator.

See its documentation for more details.
'''

import functools
import marshal

from python_toolbox import misc_tools
from python_toolbox.third_party.decorator import decorator as decorator_

from . import base_profile
from . import profile_handling


def profile(statement, globals_, locals_):
    '''Profile a statement and return the `Profile`.'''
    profile_ = base_profile.Profile()
    result = None
    try:
        profile_ = profile_.runctx(statement, globals_, locals_)
    except SystemExit:
        pass
    profile_.create_stats()
    return profile_


def profile_expression(expression, globals_, locals_):
    '''Profile an expression, and return a tuple of `(result, profile)`.'''
    profile_ = profile('result = %s' % expression, globals_, locals_)
    return (locals_['result'], profile_)


def profile_ready(condition=None, off_after=True, profile_handler=None):
    '''
    Decorator for setting a function to be ready for profiling.

    For example:

        @profile_ready()
        def f(x, y):
            do_something_long_and_complicated()

    The advantages of this over regular `cProfile` are:

     1. It doesn't interfere with the function's return value.

     2. You can set the function to be profiled *when* you want, on the fly.

     3. You can have the profile results handled in various useful ways.

    How can you set the function to be profiled? There are a few ways:

    You can set `f.profiling_on=True` for the function to be profiled on the
    next call. It will only be profiled once, unless you set
    `f.off_after=False`, and then it will be profiled every time until you set
    `f.profiling_on=False`.

    You can also set `f.condition`. You set it to a condition function taking
    as arguments the decorated function and any arguments (positional and
    keyword) that were given to the decorated function. If the condition
    function returns `True`, profiling will be on for this function call,
    `f.condition` will be reset to `None` afterwards, and profiling will be
    turned off afterwards as well. (Unless, again, `f.off_after` is set to
    `False`.)

    Using `profile_handler` you can say what will be done with profile results.
    If `profile_handler` is an `int`, the profile results will be printed, with
    the sort order determined by `profile_handler`. If `profile_handler` is a
    directory path, profiles will be saved to files in that directory. If
    `profile_handler` is details on how to send email, the profile will be sent
    as an attached file via email, on a separate thread.

    To send email, supply a `profile_handler` like so, with values separated by
    newlines:

       'ram@rachum.com\nsmtp.gmail.com\nsmtp_username\nsmtppassword'

    '''


    def decorator(function):

        def inner(function, *args, **kwargs):

            if decorated_function.condition is not None:

                if decorated_function.condition is True or \
                   decorated_function.condition(
                       decorated_function.original_function,
                       *args,
                       **kwargs
                       ):

                    decorated_function.profiling_on = True

            if decorated_function.profiling_on:

                if decorated_function.off_after:
                    decorated_function.profiling_on = False
                    decorated_function.condition = None

                # This line puts it in locals, weird:
                decorated_function.original_function

                result, profile_ = profile_expression(
                    'decorated_function.original_function(*args, **kwargs)',
                    globals(), locals()
                )

                decorated_function.profile_handler(profile_)

                return result

            else: # decorated_function.profiling_on is False

                return decorated_function.original_function(*args, **kwargs)

        decorated_function = decorator_(inner, function)

        decorated_function.original_function = function
        decorated_function.profiling_on = None
        decorated_function.condition = condition
        decorated_function.off_after = off_after
        decorated_function.profile_handler = \
                          profile_handling.get_profile_handler(profile_handler)

        return decorated_function

    return decorator

