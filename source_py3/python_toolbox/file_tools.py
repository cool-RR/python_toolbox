# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

try:
    import pathlib
except:
    from python_toolbox.third_party import pathlib

import os
import re

from python_toolbox import cute_iter_tools
from python_toolbox import context_management


N_MAX_ATTEMPTS = 100

numbered_name_pattern = re.compile(
    r'''(?P<raw_name>.*) \((?P<number>[0-9]+)\)'''
)

def _get_next_path(path):
    r'''
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
        
        
def atomic_create_and_write(path, data=None, binary=False):
    '''
    Write data to file, but use a temporary file as a buffer.
    
    The data you write to this file is actuall written to a temporary file in
    the same folder, and only after you close it, without having an exception
    raised, it renames the temporary file to your original file name. If an
    exception was raised during writing it deletes the temporary file.
    
    This way you're sure you're not getting a half-baked file.
    '''    
    with atomic_create(path, binary=binary) as file:
        return file.write(data)


@context_management.ContextManagerType
def atomic_create(path, binary=False):
    '''
    Create a file for writing, but use a temporary file as a buffer.
    
    Use as a context manager:
    
        with atomic_create(path) as my_file:
            my_file.write('Whatever')
    
    When you write to this file it actually writes to a temporary file in the
    same folder, and only after you close it, without having an exception
    raised, it renames the temporary file to your original file name. If an
    exception was raised during writing it deletes the temporary file.
    
    This way you're sure you're not getting a half-baked file.
    '''
    path = pathlib.Path(path)
    if path.exists():
        raise Exception("There's already a file called %s" % path)
    desired_temp_file_path = path.parent / ('._%s.tmp' % path.stem)
    try:
        with create_file_renaming_if_taken(desired_temp_file_path,
                                         'xb' if binary else 'x') as temp_file:
            actual_temp_file_path = pathlib.Path(temp_file.name)
            yield temp_file
        
        # This part runs only if there was no exception when writing to the
        # file:
        if path.exists():
            raise Exception("There's already a file called %s" % path)
        actual_temp_file_path.rename(path)
        assert path.exists()
        
    finally:
        if actual_temp_file_path.exists():
            actual_temp_file_path.unlink()
            

