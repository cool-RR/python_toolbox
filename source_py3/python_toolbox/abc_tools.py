# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines tools related to abstract base classes from the `abc` module.'''


class AbstractStaticMethod(staticmethod):
    '''
    A combination of `abc.abstractmethod` and `staticmethod`.

    A method which (a) doesn't take a `self` argument and (b) must be
    overridden in any subclass if you want that subclass to be instanciable.

    This class is good only for documentation; it doesn't enforce overriding
    methods to be static.
    '''
    __slots__ = ()
    __isabstractmethod__ = True

    def __init__(self, function):
        super().__init__(function)
        function.__isabstractmethod__ = True
