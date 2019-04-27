# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.


from python_toolbox import caching
from python_toolbox.misc_tools import do_nothing

from .freezer_property_freezer import FreezerPropertyFreezer
from .freezer import Freezer


class FreezerProperty(caching.CachedProperty):
    '''
    A property which lazy-creates a freezer.

    A freezer is used as a context manager to "freeze" and "thaw" an object.
    See documentation of `Freezer` in this package for more info.

    The advantages of using a `FreezerProperty` instead of creating a freezer
    attribute for each instance:

      - The `.on_freeze` and `.on_thaw` decorators can be used on the class's
        methods to define them as freeze/thaw handlers.

      - The freezer is created lazily on access (using
        `caching.CachedProperty`) which can save processing power.

    '''
    def __init__(self, on_freeze=do_nothing, on_thaw=do_nothing,
                 freezer_type=FreezerPropertyFreezer, doc=None, name=None):
        '''
        Create the `FreezerProperty`.

        All arguments are optional: You may pass in freeze/thaw handlers as
        `on_freeze` and `on_thaw`, but you don't have to. You may choose a
        specific freezer type to use as `freezer_type`, in which case you can't
        use either the `on_freeze`/`on_thaw` arguments nor the decorators.
        '''

        if freezer_type is not FreezerPropertyFreezer:
            assert issubclass(freezer_type, Freezer)
            if not (on_freeze is on_thaw is do_nothing):
                raise Exception(
                    "You've passed a `freezer_type` argument, so you're not "
                    "allowed to pass `on_freeze` or `on_thaw` arguments. The "
                    "freeze/thaw handlers should be defined on the freezer "
                    "type."
                )

        self.__freezer_type = freezer_type
        '''The type of the internal freezer. Always a subclass of `Freezer`.'''

        self._freeze_handler = on_freeze
        '''Internal freeze handler. May be a no-op.'''

        self._thaw_handler = on_thaw
        '''Internal thaw handler. May be a no-op.'''

        caching.CachedProperty.__init__(self,
                                        self.__make_freezer,
                                        doc=doc,
                                        name=name)

    def __make_freezer(self, obj):
        '''
        Create our freezer.

        This is used only on the first time we are accessed, and afterwards the
        freezer will be cached.
        '''
        assert obj is not None

        freezer = self.__freezer_type(obj)
        freezer.freezer_property = self
        return freezer


    def on_freeze(self, function):
        '''
        Use `function` as the freeze handler.

        Returns `function` unchanged, so it may be used as a decorator.
        '''
        if self.__freezer_type is not FreezerPropertyFreezer:
            raise Exception(
                "You've passed a `freezer_type` argument, so you're not "
                "allowed to use the `on_freeze` or `on_thaw` decorators. The "
                "freeze/thaw handlers should be defined on the freezer "
                "type."
            )
        self._freeze_handler = function
        return function


    def on_thaw(self, function):
        '''
        Use `function` as the thaw handler.

        Returns `function` unchanged, so it may be used as a decorator.
        '''
        if self.__freezer_type is not FreezerPropertyFreezer:
            raise Exception(
                "You've passed a `freezer_type` argument, so you're not "
                "allowed to use the `on_freeze` or `on_thaw` decorators. The "
                "freeze/thaw handlers should be defined on the freezer "
                "type."
            )
        self._thaw_handler = function
        return function


