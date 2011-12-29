# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for pickling and unpickling.'''


import re
import cPickle as pickle_module
import pickle # Importing just to get dispatch table, not pickling with it.
import copy_reg
import types

from garlicsim.general_misc import address_tools
from garlicsim.general_misc import misc_tools


def is_atomically_pickleable(thing):
    '''
    Return whether `thing` is an atomically pickleable object.
    
    "Atomically-pickleable" means that it's pickleable without considering any
    other object that it contains or refers to. For example, a `list` is
    atomically pickleable, even if it contains an unpickleable object, like a
    `threading.Lock()`.
    
    However, the `threading.Lock()` itself is not atomically pickleable.
    '''
    my_type = misc_tools.get_actual_type(thing)
    return _is_type_atomically_pickleable(my_type, thing)


def _is_type_atomically_pickleable(type_, thing=None):
    '''Return whether `type_` is an atomically pickleable type.'''
    try:
        return _is_type_atomically_pickleable.cache[type_]
    except KeyError:
        pass
    
    if thing is not None:
        assert isinstance(thing, type_)
        
    # Sub-function in order to do caching without crowding the main algorithm:
    def get_result():
        
        # We allow a flag for types to painlessly declare whether they're
        # atomically pickleable:
        if hasattr(type_, '_is_atomically_pickleable'):
            return type_._is_atomically_pickleable
        
        # Weird special case: `threading.Lock` objects don't have `__class__`.
        # We assume that objects that don't have `__class__` can't be pickled.
        # (With the exception of old-style classes themselves.)
        if not hasattr(thing, '__class__') and \
           (not isinstance(thing, types.ClassType)):
            return False
        
        if not issubclass(type_, object):
            return True
        
        def assert_legit_pickling_exception(exception):
            '''Assert that `exception` reports a problem in pickling.'''
            message = exception.args[0]
            segments = [
                "can't pickle",
                'should only be shared between processes through inheritance',
                'cannot be passed between processes or pickled'
            ]
            assert any((segment in message) for segment in segments)
            # todo: turn to warning
        
        if type_ in pickle.Pickler.dispatch:
            return True
            
        reduce_function = copy_reg.dispatch_table.get(type_)
        if reduce_function:
            try:
                reduce_result = reduce_function(thing)
            except Exception, exception:
                assert_legit_pickling_exception(exception)
                return False
            else:
                return True
        
        reduce_function = getattr(type_, '__reduce_ex__', None)
        if reduce_function:
            try:
                reduce_result = reduce_function(thing, 0)
                # (The `0` is the protocol argument.)
            except Exception, exception:
                assert_legit_pickling_exception(exception)
                return False
            else:
                return True
            
        reduce_function = getattr(type_, '__reduce__', None)
        if reduce_function:
            try:
                reduce_result = reduce_function(thing)
            except Exception, exception:
                assert_legit_pickling_exception(exception)
                return False
            else:
                return True
        
        return False

    result = get_result()
    _is_type_atomically_pickleable.cache[type_] = result
    return result
    
_is_type_atomically_pickleable.cache = {}
 

class FilteredObject(object):
    '''Placeholder for an object that was filtered out when pickling.'''
    def __init__(self, about): 
        self.about = about 
    def __repr__(self): 
        return 'FilteredObject(%s)' % repr(self.about) 
    def __getattr__(self, key):
        return FilteredObject('%s.%s' % (self.about, key))
        

_filtered_string_pattern = re.compile(
    r'^Filtered by pickle_tools \((?P<description>.*?)\)$'
)
 
class CutePickler(object): 
    '''
    Pickler which filters out non-pickleable objects.
    
    When the pickler comes upon a non-pickleable object it replaces it with a
    marker which will cause it to become a `FilteredObject` upon unpickling.
    
    (Not subclassing `cPickle.Pickler` because it doesn't support subclassing.)
    '''
    def __init__(self, file_, protocol=0): 
        pickler = self.pickler = pickle_module.Pickler(file_, protocol) 
        pickler.persistent_id = self.persistent_id
        self.dump, self.clear_memo = \
            pickler.dump, pickler.clear_memo

        
    def persistent_id(self, obj):
        if self.pre_filter:
            passed_pre_filter = self.pre_filter(obj)
        else:
            passed_pre_filter = True
        
        if passed_pre_filter and is_atomically_pickleable(obj): 
            return None 
        else:
            return 'Filtered by pickle_tools (%s)' % \
                   address_tools.describe(obj)
        
    def pre_filter(self, thing):
        '''Pre-filter `thing`, returning `False` if it shouldn't be pickled.'''
        return True
 
    
class CuteUnpickler(object): 
    '''
    Unpickler which replaces non-pickleable objects with `FilteredObject`s.
    
    When the corresponding `CutePickler` came upon non-pickleable objects it
    replacef them with a markers which will cause `CuteUnpickler` to replace
    them with `FilteredObject` instances upon unpickling.
    
    (Not subclassing `cPickle.Unpickler` because it doesn't support
    subclassing.)
    '''
    def __init__(self, file_): 
        unpickler = self.unpickler = pickle_module.Unpickler(file_) 
        unpickler.persistent_load = self.persistent_load
        self.load = unpickler.load
        self.noload = getattr(unpickler, 'noload', None)
        # (Defaulting to `None` because `pickle.Unpickler` doesn't have
        # `noload`.)

    def persistent_load(self, id_string):
        match = _filtered_string_pattern.match(id_string)
        if match:
            description = match.groupdict()['description']            
            return FilteredObject(description) 
        else: 
            raise pickle_module.UnpicklingError('Invalid persistent id')
 
 
    