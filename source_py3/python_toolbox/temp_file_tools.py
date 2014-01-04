# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to temporary files.'''

import tempfile
import shutil
import os
import pathlib

from python_toolbox import address_tools
from python_toolbox import os_tools 
from python_toolbox.context_management import ContextManager


class TemporaryFolder(ContextManager, os_tools.path_type):
    '''
    Context manager that creates a temporary folder and deletes it after usage.
    
    After the suite finishes, the temporary folder and all its files and
    subfolders will be deleted.
    
    The `TemporaryFolder` object is also a `pathlib.Path` object, so all
    operations that can be done on paths, can be done on it seamlessly.
    
    Example:
    
        with TemporaryFolder() as temporary_folder:
            
            # We have a temporary folder!
            assert temporary_folder.is_dir()
            
            # We can create files in it:
            with (temporary_folder / 'my_file').open('w') as my_file:
                my_file.write('whatever')
            
        # The suite is finished, now it's all cleaned:
        assert not temporary_folder.exists()
       
    Use the `suffix` and `prefix` string arguments to dictate a suffix and/or a
    prefix to the temporary folder's name in the filesystem.        
    '''
    
    _was_entered = False
    
    def __init__(self, prefix=tempfile.template, suffix=''):
        self.temporary_folder_prefix = prefix
        self.temporary_folder_suffix = suffix
        self.path = None
        self._closed = False
        self.__set_path(str(os_tools.null_path))
        self._init()

        
    def __enter__(self):
        assert not self._closed
        self.__set_path(
            tempfile.mkdtemp(prefix=self.temporary_folder_prefix,
                             suffix=self.temporary_folder_suffix,)
        )
        
        assert self.is_dir()
        self._was_entered = True
        return self

    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        assert not self._closed
        shutil.rmtree(str(self))
        self._closed = True
        
    def __set_path(self, path):
        self._drv, self._root, self._parts = self._parse_args((path,))
        self._str = \
                  self._format_parsed_parts(self._drv, self._root, self._parts)
        
        
    def __repr__(self):
        return '<%s: %s>' % (
            address_tools.describe(type(self), shorten=True),
            str(self) if self._was_entered else '(Not created yet)',
        )
