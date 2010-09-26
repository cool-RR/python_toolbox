import collections


class StepFunctionsToArgumentDicts(collections.defaultdict):
    def __init__(self, dict_or_iterable={}):
        collections.defaultdict.__init__(default_factory=self.default_factory)
        self.update(dict(dict_or_iterable))