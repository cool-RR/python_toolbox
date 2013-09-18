# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `VersionInfo` class.

See its documentation for more details.
'''

from operator import itemgetter as _itemgetter
from python_toolbox.nifty_collections import OrderedDict


class VersionInfo(tuple):
    '''
    Version number. This is a variation on a `namedtuple`.
    
    Example:
    
        VersionInfo(1, 2, 0) == \
            VersionInfo(major=1, minor=2, micro=0, modifier='release') == \
            (1, 2, 0)
    '''
    
    __slots__ = () 

    
    _fields = ('major', 'minor', 'micro', 'modifier') 

    
    def __new__(cls, major, minor=0, micro=0, modifier='release'):
        '''
        Create new instance of `VersionInfo(major, minor, micro, modifier)`.
        '''
        assert isinstance(major, int)
        assert isinstance(minor, int)
        assert isinstance(micro, int)
        assert isinstance(modifier, str)
        return tuple.__new__(cls, (major, minor, micro, modifier)) 

    
    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        '''Make a new `VersionInfo` object from a sequence or iterable.'''
        result = new(cls, iterable)
        if len(result) != 4:
            raise TypeError('Expected 4 arguments, got %d' % len(result))
        return result 

    
    def __repr__(self):
        '''Return a nicely formatted representation string.'''
        return 'VersionInfo(major=%r, minor=%r, micro=%r, modifier=%r)' % self

    
    def _asdict(self):
        '''
        Return a new `OrderedDict` which maps field names to their values.
        '''
        return OrderedDict(zip(self._fields, self))

    
    def _replace(self, **kwargs):
        '''
        Make a `VersionInfo` object replacing specified fields with new values.
        '''
        result = \
            self._make(map(kwargs.pop, ('major', 'minor', 'micro', 'modifier'),
                           self))
        if kwargs:
            raise ValueError('Got unexpected field names: %r' % kwargs.keys())
        return result 
    
    
    def __getnewargs__(self):
        '''Return self as a plain tuple. Used by copy and pickle.'''
        return tuple(self)
    
    @property
    def version_text(self):
        '''A textual description of the version, like '1.4.2 beta'.'''
        version_text = '%s.%s.%s' % (self.major, self.minor, self.micro)
        if self.modifier != 'release':
            version_text += ' %s' % self.modifier
        return version_text
    
    
    major = property(_itemgetter(0))
    
    minor = property(_itemgetter(1))
    
    micro = property(_itemgetter(2))

    modifier = property(_itemgetter(3))
    