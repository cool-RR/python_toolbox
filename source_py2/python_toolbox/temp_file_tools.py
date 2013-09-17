# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to temporary files.'''


import tempfile
import shutil
import os

from python_toolbox.context_management import ContextManager



class TemporaryFolder(ContextManager):
    '''
    Context manager that creates a temporary folder and deletes it after usage.
    
    After the suite finishes, the temporary folder and all its files and
    subfolders will be deleted.
    
    Example:
    
        with TemporaryFolder() as temporary_folder_path:
            
            # We have a temporary folder!
            assert os.path.isdir(temporary_folder_path)
            
            # We can create files in it:
            open(os.path.join(temporary_folder_path, 'my_file'), 'w')
            
        # The suite is finished, now it's all cleaned:
        assert not os.path.exists(temporary_folder_path)
       
    Use the `suffix` and `prefix` string arguments to dictate a suffix and/or a
    prefix to the temporary folder's name in the filesystem.        
    '''

    def __init__(self, suffix='', prefix=tempfile.template):
        self.suffix = suffix
        self.prefix = prefix
        self.path = None
        self._closed = False

        
    def __enter__(self):
        assert not self._closed
        self.path = tempfile.mkdtemp(suffix=self.suffix, prefix=self.prefix)
        assert os.path.isdir(self.path)
        return self.path

    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        assert not self._closed
        shutil.rmtree(self.path)
        self._closed = True
        
    
    def __str__(self):        
        return self.path or ''
