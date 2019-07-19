# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import abc

from .context_manager_type_type import ContextManagerTypeType


class ContextManagerType(abc.ABCMeta, metaclass=ContextManagerTypeType):
    '''
    Metaclass for `ContextManager`.

    Use this directly as a decorator to create a `ContextManager` from a
    generator function.

    Example:

        @ContextManagerType
        def MyContextManager():
            # preparation
            try:
                yield
            finally:
                pass # cleanup

    The resulting context manager could be called either with the `with`
    keyword or by using it as a decorator to a function.

    For more details, see documentation of the containing module,
    `python_toolbox.context_manager`.
    '''

    def __new__(mcls, name, bases, namespace):
        '''
        Create either `ContextManager` itself or a subclass of it.

        For subclasses of `ContextManager`, if a `manage_context` method is
        available, we will use `__enter__` and `__exit__` that will use the
        generator returned by `manage_context`.
        '''
        if 'manage_context' in namespace:
            from .context_manager import ContextManager
            manage_context = namespace['manage_context']
            if '__enter__' in namespace:
                raise Exception(
                    'You defined both an `__enter__` method and a '
                    '`manage_context` method-- That is unallowed. You need to '
                    '*either* define a `manage_context` method *or* an '
                    '`__enter__` and `__exit__` pair.'
                )
            if '__exit__' in namespace:
                raise Exception(
                    'You defined both an `__exit__` method and a '
                    '`manage_context` method-- That is unallowed. You need to '
                    '*either* define a `manage_context` method *or* an '
                    '`__enter__` and `__exit__` pair.'
                )
            namespace['__enter__'] = \
                ContextManager._ContextManager__enter_using_manage_context
            namespace['__exit__'] = \
                ContextManager._ContextManager__exit_using_manage_context

        result_class = super().__new__(mcls, name, bases, namespace)


        if (not result_class.__is_the_base_context_manager_class()) and \
           ('manage_context' not in namespace) and \
           hasattr(result_class, 'manage_context'):

            # What this `if` just checked for is: Is this a class that doesn't
            # define `manage_context`, but whose base context manager class
            # *does* define `manage_context`?
            #
            # If so, we need to be careful. It's okay for this class to be
            # using the enter/exit pair provided by the base `manage_context`;
            # It's also okay for this class to override these with its own
            # `__enter__` and `__exit__` implementations; but it's *not* okay
            # for this class to define just one of these methods, say
            # `__enter__`, because then it will not have an `__exit__` to work
            # with.

            from .context_manager import ContextManager

            our_enter_uses_manage_context = (
                result_class.__enter__ == ContextManager.\
                                    _ContextManager__enter_using_manage_context
            )

            our_exit_uses_manage_context = (
                result_class.__exit__ == ContextManager.\
                                     _ContextManager__exit_using_manage_context
            )

            if our_exit_uses_manage_context and not \
               our_enter_uses_manage_context:

                assert '__enter__' in namespace

                raise Exception(
                    f"The {result_class} class defines an `__enter__` method, "
                    f"but not an `__exit__` method; we cannot use the "
                    f"`__exit__` method of its base context manager class "
                    f"because it uses the `manage_context` generator function."
                )


            if our_enter_uses_manage_context and not \
               our_exit_uses_manage_context:

                assert '__exit__' in namespace

                raise Exception(
                    f"The {result_class} class defines an `__exit__` method, "
                    f"but not an `__enter__` method; we cannot use the "
                    f"`__enter__` method of its base context manager class "
                    f"because it uses the `manage_context` generator function."
                )

        return result_class


    def __is_the_base_context_manager_class(cls):
        '''
        Return whether `cls` is `ContextManager`.

        It's an ugly method, but unfortunately it's necessary because at one
        point we want to test if a class is `ContextManager` before
        `ContextManager` is defined in this module.
        '''

        return (
            (cls.__name__ == 'ContextManager') and
            (cls.__module__ == 'python_toolbox.context_management.'
                               'context_manager') and
            (cls.mro() == [cls, object])
        )

