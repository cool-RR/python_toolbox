# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines tools related to abstract base classes from the `abc` module.'''


class abstract_static_method(staticmethod):
    '''
    A combination of `abc.abstractmethod` and `staticmethod`.
    
    This class is good only for documentation; It doesn't enforce overriding
    methods to be static.
    '''
    __slots__ = ()
    __isabstractmethod__ = True
    
    def __init__(self, function):
        super(abstract_static_method, self).__init__(function)
        function.__isabstractmethod__ = True
