import collections

if 'OrderedDict' in vars(collections):
    from collections import OrderedDict
else:
    from .ordereddict import OrderedDict

del collections