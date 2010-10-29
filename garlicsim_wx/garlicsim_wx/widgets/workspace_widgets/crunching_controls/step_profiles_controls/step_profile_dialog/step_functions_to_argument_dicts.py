import collections


class StepFunctionsToArgumentDicts(dict):
    #tododoc: repr
    
        
    def __missing__(self, key):
        # For now this function is not very well-thought-out.
        all_dicts = self.values()
        all_dict_keys = reduce(
            set.union,
            [set(d.keys()) for d in all_dicts],
            set()
        )
        result = collections.defaultdict(lambda: '')
        for key in all_dict_keys:
            all_values = [d[key] for d in all_dicts if key in d]
            if all_values:
                value = max(all_values, key=lambda value: len(value))
                result[key] = value
        return result
        
    