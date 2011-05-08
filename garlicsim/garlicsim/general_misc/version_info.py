# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `VersionInfo` class.

See its documentation for more details.
'''

from operator import itemgetter as _itemgetter
from garlicsim.general_misc.nifty_collections import OrderedDict


class VersionInfo(tuple):
    '''
    Version number. This is a variation on a `namedtuple`.
    
    Example:
    
        VersionInfo(1, 2, 0) == \
            VersionInfo(major=1, minor=2, micro=0) == \
            (1, 2, 0)
    '''
    
    __slots__ = () 

    
    _fields = ('major', 'minor', 'micro') 

    
    def __new__(_cls, major, minor, micro):
        '''Create new instance of `VersionInfo(major, minor, micro)`.'''
        return tuple.__new__(_cls, (major, minor, micro)) 

    
    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        '''Make a new `VersionInfo` object from a sequence or iterable.'''
        result = new(cls, iterable)
        if len(result) != 3:
            raise TypeError('Expected 3 arguments, got %d' % len(result))
        return result 

    
    def __repr__(self):
        '''Return a nicely formatted representation string.'''
        return 'VersionInfo(major=%r, minor=%r, micro=%r)' % self 

    
    def _asdict(self):
        '''
        Return a new `OrderedDict` which maps field names to their values.
        '''
        return OrderedDict(zip(self._fields, self)) 

    
    def _replace(_self, **kwargs):
        '''
        Make a `VersionInfo` object replacing specified fields with new values.
        '''
        result = \
            _self._make(map(kwargs.pop, ('major', 'minor', 'micro'),_self))
        if kwargs:
            raise ValueError('Got unexpected field names: %r' % kwargs.keys())
        return result 
    
    
    def __getnewargs__(self):
        '''Return self as a plain tuple.  Used by copy and pickle.'''
        return tuple(self) 
    
    
    major = property(_itemgetter(0), doc='Alias for field number 0')
    
    
    minor = property(_itemgetter(1), doc='Alias for field number 1')
    
    
    micro = property(_itemgetter(2), doc='Alias for field number 2')