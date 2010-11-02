import cPickle as pickle_module


def filter_dict_to_picklable(d):
    new_d = d.copy()    
    for key, value in d.iteritems():
        try:
            pickle_module.dumps((key, value))
        except Exception:
            del new_d[key]
    return new_d