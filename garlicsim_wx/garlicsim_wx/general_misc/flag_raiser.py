

class FlagRaiser(object): # todo: consider renaming to show it does `Refresh`
    def __init__(self, window, attribute_name, value=True, refresh=True):
        self.window, self.attribute_name, self.value, self.refresh = \
            window, attribute_name, value, refresh
        
    def __call__(self):
        setattr(self.window, self.attribute_name, self.value)
        if self.refresh:
            self.window.Refresh()