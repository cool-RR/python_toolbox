class ResolveFailed(exceptions.GarlicSimException):
    '''An attempt to resolve a string to a Python object failed.'''
    def __init__(self, message, widget):
        self.widget = widget
        super(ResolveFailed, self).__init__(message)