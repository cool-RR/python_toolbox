'''tododoc'''

import abc

class BaseEditingInterface(obk):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def undo(self):
        pass
    
    
    # more shit here?