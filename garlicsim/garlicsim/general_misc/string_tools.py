#tododoc

import re

def camelcase_to_underscore(s):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).lower().strip('_')

def camelcase_to_spacecase(s):
    if s == '': return s
    character_process = lambda c: (' ' + c.lower()) if c.isupper() else c
    return s[0] + ''.join(character_process(c) for c in s[1:])

def underscore_to_camelcase(s):
    raise NotImplementedError



