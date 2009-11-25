

###############################################################################
import copy_reg
import types

def reduce_method(m):
    return (getattr, (m.__self__, m.__func__.__name__))

copy_reg.pickle(types.MethodType, reduce_method)
###############################################################################

import copy
import types

class Event(object):
    def __init__(self, time_left, action):
        assert time_left > 0
        self.time_left = time_left
        self.action = action
        self.done = False
        
    def pass_time(self, t):
        self.time_left -= t
        if (self.time_left <= 0)  and (not self.done):
            return self.action()
        else:
            return None
    '''   
    def __deepcopy__(self, memo):        

        if isinstance(self.action, types.MethodType):
            instance = self.action.__self__
            if instance is None: # Method is unbound
                new_action = copy.deepcopy(self.action, memo)
            
            new_instance = copy.deepcopy(self.action.__self__, memo)
            new_action = getattr(new_instance, self.action.__name__)
        else:
            new_action = copy.deepcopy(self.action, memo)
        
        censored_dict = copy.copy(self.__dict__)
        censored_dict.pop('action')
        new_dict = copy.deepcopy(censored_dict, memo)
        new_dict['action'] = new_action
        
        new_event = Event.__new__(self.__class__)
        
        new_event.__dict__.update(new_dict)
        
        return new_event
    ''' 
            
        

        

        
        
        
