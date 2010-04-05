

class FlagRaiser(object):
    def __init__(self, object, attribute_name, value=True):
        self.object, self.attribute_name, self.value = \
            object, attribute_name, value
    def __call__(self):
        setattr(object, attribute_name, value)