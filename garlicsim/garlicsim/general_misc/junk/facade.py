import cPickle

'''
class Fuga(object):
    def __init__(
'''
    
    
class Object(object):
    pass

def naturally_picklable(thing):
    try:
        cPickle.dumps(thing)
        return True
    except Exception:
        return False

def prepare_for_pickling(thing):
    if naturally_picklable(thing):
        return thing
    
    old_dict = thing.__dict__

    if hasattr(thing, "__dict__"):
        old_dict = dict(thing.__dict__)
    else:
        old_list = [[name, getattr(thing, name)] for name in dir(thing)]
        old_dict = {}
        for key, value in old_list:
            old_dict[key] = value
        
    my_object = Object()
    new_dict = my_object.__dict__ = {}
    
    for key, value in old_dict.items():
        if naturally_picklable(value):
            new_dict[key] = value
        else:
            new_dict[key] = prepare_for_pickling(value)
    
    return my_object
            

def preepy(module):
    
    old_dict = dict(module.__dict__)
        
    my_object = Object()
    new_dict = my_object.__dict__ = old_dict
    
    return my_object

def fuga(module):
    return (lambda x: x, (preepy(module),))

def dumps(thing):
    return cPickle.dumps(prepare_for_pickling(thing))
        
import copy_reg
module_type = type(copy_reg)
copy_reg.pickle(module_type, fuga)
cPickle.dumps(copy_reg)
