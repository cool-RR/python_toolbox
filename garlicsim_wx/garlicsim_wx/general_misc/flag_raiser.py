

class FlagRaiser(object):
    def __init__(self, window, attribute_name, value=True): #, refresh=True):
        self.window, self.attribute_name, self.value = \
            window, attribute_name, value
            
        # self.refresh = refresh
        
    def __call__(self):
        setattr(self.window, self.attribute_name, self.value)
        #if self.refresh:
        self.window.Refresh()