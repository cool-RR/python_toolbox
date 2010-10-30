import collections

from garlicsim.general_misc import introspection_tools
from garlicsim.general_misc import address_tools


class StepFunctionsToArgumentDicts(dict):
    #tododoc: repr
    def __init__(self, describe_function, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.describe = describe_function
        
    def __missing__(self, step_function):
        defaults = introspection_tools.get_default_args_dict(step_function)
        result = collections.defaultdict(
            lambda: '',
            dict(
                (key, self.describe(value)) for (key, value) in
                defaults.iteritems()
            )
        )
        self[step_function] = result
        return result