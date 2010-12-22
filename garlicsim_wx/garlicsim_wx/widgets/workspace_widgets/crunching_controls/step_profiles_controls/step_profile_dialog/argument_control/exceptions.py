# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines exceptions for `ArgumentControl`.'''

from garlicsim.misc import exceptions


class ResolveFailed(exceptions.GarlicSimException):
    '''An attempt to resolve a string to a Python object failed.'''
    def __init__(self, message, widget):
        self.widget = widget
        super(ResolveFailed, self).__init__(message)