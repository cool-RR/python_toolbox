#tododoc

import re

def camelcase_to_underscore(s):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).lower().strip('_')

def underscore_to_camelcase(s):
    raise NotImplementedError