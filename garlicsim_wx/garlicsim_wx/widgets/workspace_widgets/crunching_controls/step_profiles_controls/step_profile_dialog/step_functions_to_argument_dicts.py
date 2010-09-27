import collections


class StepFunctionsToArgumentDicts(collections.defaultdict):

    def __init__(self, dict_or_iterable={}):
        collections.defaultdict.__init__(self,
                                         self.default_factory,
                                         dict_or_iterable)
    
        
    def default_factory(self):
        # For now this function is not very well-thought-out.
        all_dicts = self.values()
        all_dict_keys = reduce(
            set.union,
            [set(d.keys()) for d in all_dicts]
        )
        result = collections.defaultdict(lambda: '')
        for key in all_dict_keys:
            all_values = [d[key] for d in all_dicts if key in d]
            if all_values:
                value = max(all_values, lambda value: len(repr(value)))
                result[key] = value
        return result
        
    