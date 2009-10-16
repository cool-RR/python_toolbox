import weakref


class ChangeTracker(object): 
    '''
    '''
    #todo: possible that hash won't change when object changes?
    
    def __init__(self):
        self.library = weakref.WeakKeyDictionary()
        
    def check_in(self, thing):
        if thing not in self.library:
            self.library[thing] = hash(thing)
            return True
        
        # thing in self.library
        
        previous_hash = self.library[thing]
        new_hash = hash(thing)
        if previous_hash == new_hash:
            return False
        else:
            self.library[thing] = new_hash
            return True
            