# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.


class ReasonedBool(object):
    '''
    A variation on `bool` that also gives a `.reason`.
    
    This is useful when you want to say "This is False because... (reason.)"
    
    Unfortunately this class is not a subclass of `bool`, since Python doesn't
    allow subclassing `bool`.    
    '''

    def __init__(self, value, reason=None):
        '''
        Construct the `ReasonedBool`.
        
        `reason` is the reason *why* it has a value of `True` or `False`. It is
        usually a string, but is allowed to be of any type.
        '''
        self.value = bool(value)
        self.reason = reason
        
        
    def __repr__(self):
        if self.reason is not None:
            return '<%s because %s>' % (self.value, repr(self.reason))
        else: # self.reason is None
            return '<%s with no reason>' % self.value

        
    def __eq__(self, other):
        return bool(self) == other
    
    
    def __hash__(self):
        return hash(bool(self))
    
    
    def __neq__(self, other):
        return not self.__eq__(other)

    
    def __bool__(self):
        return self.value
    __nonzero__ = __bool__