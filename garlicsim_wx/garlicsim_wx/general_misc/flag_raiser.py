

class FlagRaiser(object): # todo: consider renaming to show it does `Refresh`
    def __init__(self, window, attribute_name, value=True):
        self.window, self.attribute_name, self.value = \
            window, attribute_name, value
    def __call__(self):
        setattr(self.window, self.attribute_name, self.value)
        self.window.Refresh()