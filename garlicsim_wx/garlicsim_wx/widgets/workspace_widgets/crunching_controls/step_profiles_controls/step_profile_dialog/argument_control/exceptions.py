# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines exceptions for `ArgumentControl`.'''

from garlicsim.misc import exceptions


class ResolveFailed(exceptions.GarlicSimException):
    '''An attempt to resolve a string to a Python object failed.'''
    def __init__(self, message, widget):
        self.widget = widget
        super(ResolveFailed, self).__init__(message)