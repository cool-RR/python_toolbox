
class abstract_static_method(staticmethod):
    
    __slots__ = ()
    __isabstractmethod__ = True
    
    def __init__(self, function):
        super(abstract_static_method, self).__init__(function)
        function.__isabstractmethod__ = True
