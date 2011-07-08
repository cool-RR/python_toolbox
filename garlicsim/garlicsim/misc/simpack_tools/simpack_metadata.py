# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackMetadata` class.

See its documentation for more information.
'''

import garlicsim.general_misc.third_party.namedtuple

from garlicsim.general_misc import module_tasting
from garlicsim.general_misc import caching


_SimpackMetadataBase = garlicsim.general_misc.\
                       third_party.namedtuple.namedtuple(
                           '_SimpackMetadataBase',
                           'address name version description tags',
                       )


class SimpackMetadata(_SimpackMetadataBase):
    
    def __init__(self, *args, **kwargs):
        
        _SimpackMetadataBase.__init__(self)
        # Not passing arguments to `_SimpackMetadataBase.__init__` because it's
        # actually `object.__init__`.
        
        assert isinstance(self.address, basestring) or self.address is None
        assert isinstance(self.name, basestring) or self.name is None
        assert isinstance(self.version, basestring) or self.version is None
        assert isinstance(self.description, basestring) or self.description \
                                                                        is None
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


    @caching.cache()
    def matches_filter_words(self, filter_words):
        return all(self._matches_filter_word(word) for word in filter_words)

    
    @caching.cache()
    def _matches_filter_word(self, word):
        assert isinstance(word, basestring)
        texts_to_search = filter(None, (self.address, self.name, self.version,
                                        self.description) + (self.tags or ()))
        return any(word in text_to_search for text_to_search in
                   texts_to_search)
