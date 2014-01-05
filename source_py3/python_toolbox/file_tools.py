# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to temporary files.'''

import pathlib
import re


numbered_name_pattern = re.compile(
    r'''(?P<raw_name>.*) \((?P<number>[0-9]+)\)'''
)

def _get_next_name(path):
    assert isinstance(path, pathlib.Path)
    parent = path.parent
    suffix = path.suffix
    suffixless_name = path.name[:-len(suffix)]
    assert parent + suffix + suffixless_name == path
    match = numbered_name_pattern.match(suffixless_name)
    if match:
        fixed_suffixless_name = '{} ({})'.format(
            match.group('raw_name'),
            int(match.group('number'))+1,
        )
    else:
        fixed_suffixless_name = '{} (1)'.format(suffixless_name,)
        fix
    return pathlib.Path(
        '{}{}{}'.format(parent, suffixless_name, suffix)
    )
    
    

def create_file_renaming_if_taken(path, binary=False):
    path = pathlib.Path(path)
    

