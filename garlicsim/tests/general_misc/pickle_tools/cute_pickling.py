import threading, multiprocessing
from cStringIO import StringIO 
import tempfile

# We're importing `pickle_module` from `pickle_tools`, so we get the exact same
# pickle module it's using. (Giving it the freedom to change between `cPickle`
# and `pickle`.)
from garlicsim.general_misc.pickle_tools import pickle_module

import wx

from garlicsim.general_misc import pickle_tools
from garlicsim.general_misc.pickle_tools import CutePickler, CuteUnpickler


#class ComparableObject(Object):
    #def __eq__(self, other):
        #return type(self) is type(other) and \
               #vars(self) == vars(other)
    #pass


def test_totally_pickleable():
    
    
    totally_pickleable_things = [
        [1, 2, (3, 4)],
        {1: 2, 3: set((1, 2, 3))},
        None, True, False,
        (1, 2, 'meow'),
        u'qweqweqasd',
    ]
    
    for thing in totally_pickleable_things:
        stream = StringIO() 
        pickler = CutePickler(stream)
        pickler.dump(thing) 
 
        stream.seek(0) 
        unpickler = CuteUnpickler(stream) 
        unpickled_thing = unpickler.load() 
        assert unpickled_thing == thing