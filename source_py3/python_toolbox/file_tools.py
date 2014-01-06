# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to temporary files.'''

import pathlib
import os
import re

from python_toolbox import cute_iter_tools
from python_toolbox import context_management


N_MAX_ATTEMPTS = 100

numbered_name_pattern = re.compile(
    r'''(?P<raw_name>.*) \((?P<number>[0-9]+)\)'''
)

def _get_next_path(path):
    '''
    Get the name that `path` should be renamed to if taken.
    
    For example, "c:\example.ogg" would become "c:\example (1).ogg", while
    "c:\example (1).ogg" would become "c:\example (2).ogg".
    
    (Uses `Path` objects rather than strings.)
    '''
    assert isinstance(path, pathlib.Path)
    suffix = path.suffix
    stem = path.stem
    parent_with_separator = str(path)[:-len(path.name)]
    assert pathlib.Path('{}{}{}'.format(parent_with_separator,
                                        stem, suffix)) == path
    match = numbered_name_pattern.match(stem)
    if match:
        fixed_stem = '{} ({})'.format(
            match.group('raw_name'),
            int(match.group('number'))+1,
        )
    else:
        fixed_stem = '{} (1)'.format(stem,)
    return pathlib.Path(
        '{}{}{}'.format(parent_with_separator, fixed_stem, suffix)
    )


def iterate_file_paths(path):
    '''
    Iterate over file paths, hoping to find one that's available.
    
    For example, when given "c:\example.ogg", would first yield
    "c:\example.ogg", then "c:\example (1).ogg", then "c:\example (2).ogg", and
    so on.
    
    (Uses `Path` objects rather than strings.)
    '''
    while True:
        yield path
        path = _get_next_path(path)
    
    
def create_folder_renaming_if_taken(path):
    '''
    Create a new folder with name `path`, renaming it if name taken.
    
    If the name given is "example", the new name would be "example (1)", and if
    that's taken "example (2)", and so on.
    
    Returns a path object to the newly-created folder.
    '''
    for path in cute_iter_tools.shorten(iterate_file_paths(pathlib.Path(path)),
                                        N_MAX_ATTEMPTS):
        try:
            os.makedirs(str(path), exist_ok=False)
        except OSError:
            pass
        else:
            return path
    else:
        raise Exception("Exceeded {} tries, can't create folder {}".format(
            N_MAX_ATTEMPTS,
            path
        ))
    

def create_file_renaming_if_taken(path, mode='x',
                                  buffering=-1, encoding=None,
                                  errors=None, newline=None):
    '''
    Create a new file with name `path` for writing, renaming it if name taken.
    
    If the name given is "example.zip", the new name would be "example
    (1).zip", and if that's taken "example (2).zip", and so on.
    
    Returns the file open and ready for writing. It's best to use this as a
    context manager similarly to `open` so the file would be closed.
    '''
    assert 'x' in mode
    for path in cute_iter_tools.shorten(iterate_file_paths(pathlib.Path(path)),
                                        N_MAX_ATTEMPTS):
        try:
            return path.open(mode, buffering=buffering,
                                     encoding=encoding, errors=errors,
                                     newline=newline)
        except FileExistsError:
            pass
    else:
        raise Exception("Exceeded {} tries, can't create file {}".format(
            N_MAX_ATTEMPTS,
            path
        ))
    

def write_to_file_renaming_if_taken(path, data, mode='x',
                                    buffering=-1, encoding=None,
                                    errors=None, newline=None):
    '''
    Write `data` to a new file with name `path`, renaming it if name taken.
    
    If the name given is "example.zip", the new name would be "example
    (1).zip", and if that's taken "example (2).zip", and so on.
    '''
    with create_file_renaming_if_taken(
        path, mode=mode, buffering=buffering, encoding=encoding, errors=errors,
        newline=newline) as file:
        
        return file.write(data)
        