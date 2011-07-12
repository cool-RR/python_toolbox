# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackPlace` class.

See its documentation for more information.
'''

import os

import garlicsim.general_misc.third_party.namedtuple

from garlicsim.general_misc import module_tasting
from garlicsim.general_misc import caching
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import package_finder
from garlicsim.general_misc import address_tools

from garlicsim.misc.simpack_tools import SimpackMetadata


_SimpackPlaceBase = garlicsim.general_misc.\
                       third_party.namedtuple.namedtuple(
                           '_SimpackPlaceBase',
                           'path package_prefix name',
                       )


class SimpackPlace(_SimpackPlaceBase):
    '''
    A place on the filesystem where simpacks are stored.
    
    A simpack place is defined not only by a path, but also by an optional
    `.package_prefix`. When defined, it specifies the package prefix that
    contains the simpacks. For example, in GarlicSim's simpack library, the
    package prefix is `garlicsim_lib.simpacks.`.
    
    A simpack place also has a `.name` which is a user-friendly name.
    '''
    
    __metaclass__ = caching.CachedType
    
    
    def __new__(self, path, package_prefix='', name=None):
        # Using `__new__` instead of `__init__` because that's what
        # `namedtuple` uses and we need to preempt their logic.
        
        ### Determining name: #################################################
        #                                                                     #
        if name is None:
            if package_prefix:
                parent_package = address_tools.resolve(package_prefix[:-1])
                if hasattr(parent_package, 'simpack_place_name'):
                    name = getattr(parent_package, 'simpack_place_name')
            else:
                name = os.path.split(path)[-1]
        #                                                                     #
        ### Finished determining name. ########################################
        
        simpack_place = _SimpackPlaceBase.__new__(
            SimpackPlace,
            path=path,
            package_prefix=package_prefix,
            name=name
        )
            
        return simpack_place

    
    def __init__(self, path, package_prefix='', name=None):
        '''Construct a new `SimpackPlace`.'''
        # Defining `__init__` mostly to satisfy `CachedType`.

        _SimpackPlaceBase.__init__(self)
        # Not passing arguments to `_SimpackPlaceBase.__init__` because it's
        # actually `object.__init__`.
                
        assert isinstance(self.path, basestring)
        assert isinstance(self.package_prefix, basestring)
        assert isinstance(self.name, basestring)
        
        if False: # This section gives us better source assistance in Wing IDE:
            self.path = self.path
            self.package_prefix = self.package_prefix
            self.name = self.name
            
            
    def get_simpack_metadatas(self):
        '''
        Get the metadatas of all the simpacks contained in this simpack place.
        
        Returns a list of `SimpackMetadata` objects.
        '''
        
        ### Determining path to search: ###################################
        #                                                                 #
        if self.package_prefix:
            assert self.package_prefix.endswith('.')
            package = address_tools.resolve(self.package_prefix[:-1])
            path_to_search = path_tools.get_path_of_package(package)
        else: # not self.package_prefix
            path_to_search = self.path
        #                                                                 #
        ### Finished determining path to search. ##########################
            
        simpack_addresses = [
            (self.package_prefix + module_name[1:]) for module_name in
            package_finder.get_module_names(path_to_search)
        ]
        
        return map(SimpackMetadata.create_from_address, simpack_addresses)
    
    
    @caching.CachedProperty
    def _text_to_search(self):
        '''
        The total mass of search that should be searched in.
        
        Contains the name, the package prefix, and the path.
        '''
        return ''.join([text.lower() for text in
                        (self.name, self.package_prefix, self.path)
                        if text is not None])

    @caching.cache()
    def matches_filter_words(self, filter_words):
        '''
        Do all of the filter words appear in this simpack places's text?
        
        `filter_words` is a list of strings, such as `['library',
        'garlicsim']`. Returns `True` if and only if every word appears
        somewhere in this simpack place's text.
        '''
        return all(self._matches_filter_word(word) for word in filter_words)

    
    @caching.cache()
    def _matches_filter_word(self, word):
        '''Does `word` appear in this simpack place's text?'''
        assert isinstance(word, basestring)
        lower_word = word.lower()
        return lower_word in self._text_to_search
