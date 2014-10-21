# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to temporary files.'''

import tempfile
import shutil
try:
    import pathlib
except:
    from python_toolbox.third_party import pathlib


from python_toolbox import context_management 


@context_management.ContextManagerType
def create_temp_folder(suffix='', prefix=tempfile.template):
    '''
    Context manager that creates a temporary folder and deletes it after usage.
    
    After the suite finishes, the temporary folder and all its files and
    subfolders will be deleted.
    
    Example:
    
        with create_temp_folder() as temp_folder:
            
            # We have a temporary folder!
            assert temp_folder.is_dir()
            
            # We can create files in it:
            (temp_folder / 'my_file').open('w')
            
        # The suite is finished, now it's all cleaned:
        assert not temp_folder.exists()
       
    Use the `suffix` and `prefix` string arguments to dictate a suffix and/or a
    prefix to the temporary folder's name in the filesystem.        
    '''
    temp_folder = pathlib.Path(tempfile.mkdtemp(suffix=suffix, prefix=prefix))
    yield temp_folder
    shutil.rmtree(str(temp_folder))
