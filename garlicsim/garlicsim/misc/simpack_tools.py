# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for working with simpacks.'''

from garlicsim.general_misc import address_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import caching
from garlicsim.general_misc import nifty_collections
from garlicsim.general_misc import module_tasting


import garlicsim.misc.simpack_grokker


def get_from_state(state):
    '''Find the simpack that a state class (or a state instance) belong to.'''
    state_class = state if isinstance(state, type) else type(state)
    return _get_from_state_class(state_class)
    

@caching.cache()
def _get_from_state_class(state_class):
    '''
    Find the simpack that a state class belongs to.
    
    Internal use.
    '''
    assert state_class.__name__ == 'State' # remove this limitation
    short_address = address_tools.describe(state_class, shorten=True)
    simpack_name = '.'.join(short_address.split('.')[:-1])
    simpack = import_tools.normal_import(simpack_name)
        
    garlicsim.misc.simpack_grokker.SimpackGrokker(simpack)
    # Not saving the reference: But it'll get cached because `SimpackGrokker`
    # is a `CachedType`.
        
    return simpack


_SimpackMetadataBase = garlicsim.general_misc.third_party.namedtuple.namedtuple(
    '_SimpackMetadataBase',
    'address name version description tags',
)

class SimpackMetadata(_SimpackMetadataBase):
    
    def __init__(self, *args, **kwargs):
        
        _SimpackMetadataBase.__init__(self, *args, **kwargs)
        
        assert isinstance(self.address, basestring) or self.address is None
        assert isinstance(self.name, basestring) or self.name is None
        assert isinstance(self.version, basestring) or self.version is None
        assert isinstance(self.description, basestring) or self.description is None
        assert isinstance(self.tags, tuple) or self.tags is None        
        
        
        if False: # This section gives us better source assistance in Wing IDE:
            self.address = self.address
            self.name = self.name
            self.version = self.version
            self.description = self.description
            self.tags = self.tags
        
    
    @staticmethod
    @caching.cache()
    def create_from_address(address):
        tasted_simpack = module_tasting.taste_module(address)
        name = getattr(tasted_simpack, 'name', address.rsplit('.')[-1])
        version = getattr(tasted_simpack, 'name', None)
        description = getattr(tasted_simpack, '__doc__', None)
        tags = getattr(tasted_simpack, 'tags', None)
        return SimpackMetadata(address=address,
                               name=name,
                               version=version,
                               description=description,
                               tags=tags)



