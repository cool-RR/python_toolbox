# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackMetadata` class.

See its documentation for more information.
'''

import zipimport

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
    '''
    Metadata about a simpack, including name, version, address and description.
    
    The most important feature of this class is that it obtains all the
    metadata *without* importing the simpack. (It does that using
    module-tasting.) This is very useful because we want to get metadata about
    a lot of simpacks, but we don't want to import them all. We want to import
    only the one that we'll choose to work with.
    '''
    
    @staticmethod
    @caching.cache()
    def create_from_address(address):
        '''Create a `SimpackMetadata` from the address of a simpack.'''
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
        else:
            version = None
        #                                                                     #
        ### Finished getting version number. ##################################
        simpack_metadata = SimpackMetadata(address=address,
                                           name=name,
                                           version=version,
                                           description=description,
                                           tags=tags)
        simpack_metadata._tasted_simpack = tasted_simpack
        
        return simpack_metadata
    
    
    def __init__(self, address, name, version, description, tags):
        
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
            '''Address of the simpack, like `garlicsim_lib.simpacks.life`.'''
            
            self.name = self.name
            '''Name of the simpack, like "Conway's Game of Life.'''
            
            self.version = self.version
            '''Version of the simpack, like '0.5.2'.'''
            
            self.description = self.description
            '''Extensive description of the simpack in reStructuredText.'''
            
            self.tags = self.tags
            '''List of tags, like `['chemistry', '3d', 'heavy-cpu']`.'''
            
                    
    def import_simpack(self):
        '''
        Import the simpack and return it.
        
        The simpack may or may not be imported already. In any case after this
        function is called it will be imported and returned.
        '''
        return address_tools.resolve(self.address)
        
    
    @caching.CachedProperty
    def _text_to_search(self):
        '''
        The total mass of search that should be searched in.
        
        Contains the name, address, description and version all concatenated
        together.
        '''
        return ''.join([text.lower() for text in
                        ((self.address, self.name, self.version,
                        self.description) + (self.tags or ()))
                        if text is not None])

    
    @caching.cache()
    def matches_filter_words(self, filter_words, simpack_place=None):
        '''
        Do all of the filter words appear in this simpack metadata's text?
        
        `filter_words` is a list of strings, such as `['physics', 'discrete',
        '3d']`. Returns `True` if and only if every word appears somewhere in
        this simpack metadata's text.
        
        If `simpack_place` is given, its text would also be searched,
        (increasing the likelihood that this function would return `True`.)
        '''
        return all(self._matches_filter_word(word, simpack_place) for word in
                   filter_words)

    
    @caching.cache()
    def _matches_filter_word(self, word, simpack_place=None):
        '''
        Does `word` appear in this simpack metadata's text?
        
        If `simpack_place` is given, its text would also be searched,
        (increasing the likelihood that this function would return `True`.)
        '''
        assert isinstance(word, basestring)
        lower_word = word.lower()
        if simpack_place is not None:
            return (lower_word in self._text_to_search) or \
                   (lower_word in simpack_place._text_to_search)
        else:
            return (lower_word in self._text_to_search)
        
    
    @caching.CachedProperty
    def contains_source_files(self):
        '''Does the simpack contain the source files?'''
        return module_tasting.tasted_resources.resource_exists(
            self._tasted_simpack,
            '__init__.py'
        )

    
    @caching.CachedProperty
    def is_zip_module(self):
        '''Is the simpack a zipimported module?'''
        loader = getattr(self._tasted_simpack, '__loader__', None)
        return loader is not None and isinstance(loader, zipimport.zipimporter)
    