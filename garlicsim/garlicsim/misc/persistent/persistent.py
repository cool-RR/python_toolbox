# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Note: This module is still experimental.

todo: need to lock library to avoid thread trouble?

todo: need to raise an exception if we're getting pickled with
an old protocol?

todo: make it polite to other similar classes

todo: what happens when you want to fork-by-editing a state and change
a big 3-d model which is a PRO?
'''


import uuid
import weakref
import colorsys


__all__ = ["Persistent"]

library = weakref.WeakValueDictionary()


class UuidToken(object):
    '''
    A token which contains a uuid with its attribute .uuid
    '''
    def __init__(self, uuid):
        self.uuid = uuid

class Persistent(object):
    '''
    A class to use as a subclass for objects which do not change. When copying a
    Persistent, it is not really copied; The new "copy" is just the same object.
    When a Persistent is passed around between processes in queues, each process
    retains only one copy of it.
    
    What does it mean that the object is read-only? It means that starting from
    the first time that it is copied or put in a queue, it should not be
    changed.

    There is no mechanism that enforces that the user doesn't change the object.
    
    Note: This class is still experimental.
    '''
    def __new__(cls, *args, **kwargs):
        
        # Here we need to check in what context __new__ was called.
        # There are two options:
        #     1. The object is being created.
        #     2. The object is being unpickled.
        # We check whether we are getting a uuid token. If we are, it's
        # unpickling. If we don't, it's creation.
        
        if len(args)==1 and len(kwargs)==0 and isinstance(args[0], UuidToken):
            received_uuid = args[0].uuid
        else:
            received_uuid = None
            
        if received_uuid: # The object is being unpickled
            thing = library.pop(received_uuid, None)
            if thing:
                thing._Persistent__skip_setstate = True
                return thing
            else: # This object does not exist in our library yet; Let's add it
                thing = super(Persistent, cls).__new__(cls)
                thing._Persistent__uuid = received_uuid
                library[received_uuid] = thing
                return thing
                
        else: # The object is being created
            thing = super(Persistent, cls).__new__(cls)
            new_uuid = uuid.uuid4()
            thing._Persistent__uuid = new_uuid
            library[new_uuid] = thing
            return thing
        
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        del my_dict["_Persistent__uuid"]
        return my_dict
    
    def __getnewargs__(self):
        return (UuidToken(self._Persistent__uuid),)
    
    def __setstate__(self, state):
        if self.__dict__.pop("_Persistent__skip_setstate", None):
            return
        else:
            self.__dict__.update(state)
    
    def __deepcopy__(self, memo):
        return self
    
    def __copy__(self):
        return self
    
    def __generate_personality(self):
        '''tododoc, and all below
        
        todo: do (or find) some take_entropy library
        todo: maybe make Personality class?
        '''
        import human_names
        color_resolution = 100
        
        u = int(self.__uuid)
        
        (u, human_name_seed) = divmod(u, 5494)
        self.__human_name = human_names.name_list[human_name_seed]
        
        color_seeds = []
        for i in range(4):
            (u, new_color_seed) = divmod(u, color_resolution)
            color_seeds.append(new_color_seed)
        

        normalized_color_seeds = \
            [color_seed * (1.0/color_resolution) for color_seed in color_seeds]
        
        self.__light_color = normalized_color_seeds[0:2] + [0.9]
        self.__dark_color = normalized_color_seeds[2:4] + [0.1]
        
    
    def get_light_color(self):
        if hasattr(self, '_Persistent__light_color'):
            return self.__light_color
        else:
            self.__generate_personality()
            return self.__light_color
    
    def get_dark_color(self):
        if hasattr(self, '_Persistent__dark_color'):
            return self.__dark_color
        else:
            self.__generate_personality()
            return self.__dark_color
        
    def get_human_name(self):
        if hasattr(self, '_Persistent__human_name'):
            return self.__human_name
        else:
            self.__generate_personality()
            return self.__human_name
        

# --------------------------------------------------------------
'''
From here on it's just testing stuff; will be moved to another file.

    
    
def play_around(queue, thing):
    import copy
    queue.put((thing, copy.deepcopy(thing),))

class Booboo(Persistent):
    def __init__(self):
        self.number = random.random()
    
if __name__ == "__main__":
    
    import multiprocessing
    import random
    import copy
    
    def same(a, b):
        return (a is b) and (a == b) and (id(a) == id(b)) and \
               (a.number == b.number)
    
    a = Booboo()
    b = copy.copy(a)
    c = copy.deepcopy(a)
    assert same(a, b) and same(b, c)
    
    my_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target = play_around,
                                      args=(my_queue, a,))
    process.start()
    process.join()
    things = my_queue.get()
    for thing in things:
        assert same(thing, a) and same(thing, b) and same(thing, c)
    print("all cool!")
'''