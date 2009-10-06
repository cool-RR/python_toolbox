class ArgumentsProfile(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    def __eq__(self, other):
        return isinstance(other, ArgumentsProfile) and \
               self.args == other.args and self.kwargs == other.kwargs
               
class StepOptionsProfile(ArgumentsProfile):
    pass