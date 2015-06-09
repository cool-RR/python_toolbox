# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import pickle

from python_toolbox.nifty_collections import WeakKeyIdentityDict


class ChangeTracker(object): 
    '''
    Tracks changes in objects that are registered with it.
    
    To register an object, use `.check_in(obj)`. It will return `True`. Every
    time `.check_in` will be called with the same object, it will return
    whether the object changed since the last time it was checked in.
    '''
    
    def __init__(self):
        self.library = WeakKeyIdentityDict()
        '''dictoid mapping from objects to their last pickle value.'''
        
        
    def check_in(self, thing):
        '''        
        Check in an object for change tracking.
        
        The first time you check in an object, it will return `True`. Every
        time `.check_in` will be called with the same object, it will return
        whether the object changed since the last time it was checked in.
        '''
        
        new_pickle = cPickle.dumps(thing, 2)
        
        if thing not in self.library:
            self.library[thing] = new_pickle
            return True
        
        # thing in self.library
        
        previous_pickle = self.library[thing]
        if previous_pickle == new_pickle:
            return False
        else:
            self.library[thing] = new_pickle
            return True
    
        
    def __contains__(self, thing):
        '''Return whether `thing` is tracked.'''
        return self.library.__contains__(thing)

