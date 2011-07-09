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


_SimpackPlaceBase = garlicsim.general_misc.\
                       third_party.namedtuple.namedtuple(
                           '_SimpackPlaceBase',
                           'path package_prefix name',
                       )


class SimpackPlace(_SimpackPlaceBase):
    

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
        # Defining blank `__init__` to satisfy `CachedType`.

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
        
        ### Determining path to search: ###################################
        #                                                                 #
        if self.package_prefix:
            assert self.package_prefix.endswith('.')
            package = address_tools.resolve(package_prefix[:-1])
            path_to_search = path_tools.get_path_of_package(package)
        else: # not self.package_prefix
            path_to_search = path
        #                                                                 #
        ### Finished determining path to search. ##########################
            
        simpack_addresses = [
            (package_prefix + package_name[1:]) for package_name in
            package_finder.get_packages(path_to_search, self_in_name=False)
        ]
    

    @caching.cache()
    def matches_filter_words(self, filter_words):
        return all(self._matches_filter_word(word) for word in filter_words)

    
    @caching.cache()
    def _matches_filter_word(self, word):
        assert isinstance(word, basestring)
        texts_to_search = filter(
            None,
            (self.name, self.package_prefix, self.path)
        )
        return any(word in text_to_search for text_to_search in
                   texts_to_search)
