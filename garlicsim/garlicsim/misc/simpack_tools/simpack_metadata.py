# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackMetadata` class.

See its documentation for more information.
'''

import garlicsim.general_misc.third_party.namedtuple

from garlicsim.general_misc import module_tasting
from garlicsim.general_misc import address_tools
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
        description = getattr(tasted_simpack, '__doc__', None)
        tags = getattr(tasted_simpack, 'tags', None)
        ### Getting version number: ###########################################
        #                                                                     #
        if hasattr(tasted_simpack, '__version__'):            
            version = getattr(tasted_simpack, '__version__')
        elif '.' in address:
            root_address = address.split('.', 1)[0]
            root_package = address_tools.resolve(root_address)
            version = getattr(root_package, '__version__', None)
        #                                                                     #
        ### Finished getting version number. ##################################
        simpack_metadata = SimpackMetadata(address=address,
                                           name=name,
                                           version=version,
                                           description=description,
                                           tags=tags)
        simpack_metadata._tasted_simpack = tasted_simpack
        return simpack_metadata
        
    
    @caching.CachedProperty
    def _text_to_search(self):
        return ''.join([text.lower() for text in
                        ((self.address, self.name, self.version,
                        self.description) + (self.tags or ()))
                        if text is not None])

    
    @caching.cache()
    def matches_filter_words(self, filter_words, simpack_place=None):
        return all(self._matches_filter_word(word, simpack_place) for
                   word in filter_words)

    
    @caching.cache()
    def _matches_filter_word(self, word, simpack_place=None):
        assert isinstance(word, basestring)
        lower_word = word.lower()
        if simpack_place is not None:
            return (lower_word in self._text_to_search) or \
                   (lower_word in simpack_place._text_to_search)
        else:
            return (lower_word in self._text_to_search)
