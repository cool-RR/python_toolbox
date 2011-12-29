# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Various zip-related tools.'''

from __future__ import with_statement

import contextlib
import zipfile
import os.path
import re
import fnmatch


def zip_folder(folder, zip_path, ignored_patterns=[]):
    '''
    Zip `folder` into a zip file specified by `zip_path`.
    
    Note: Creates a folder inside the zip with the same name of the original
    folder, in contrast to other implementation which put all of the files on
    the root level of the zip.
    
    `ignored_patterns` are fnmatch-style patterns specifiying file-paths to
    ignore.
    
    Any empty sub-folders will be ignored.
    '''
    assert os.path.isdir(folder)
    source_folder = os.path.realpath(folder)
    
    ignored_re_patterns = [re.compile(fnmatch.translate(ignored_pattern)) for
                           ignored_pattern in ignored_patterns]
    
    zip_name = os.path.splitext(os.path.split(zip_path)[1])[0]
    source_folder_name = os.path.split(source_folder)[1]
            
    with contextlib.closing(
        zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        ) as zip_file:
        
        for root, subfolders, files in os.walk(source_folder):
            
            for file_path in files:
                
                if any(ignored_re_pattern.match(os.path.join(root, file_path))
                       for ignored_re_pattern in ignored_re_patterns):
                    continue
                
                absolute_file_path = os.path.join(root, file_path)
                
                destination_file_path = os.path.join(
                    source_folder_name,
                    absolute_file_path[(len(source_folder) + len(os.sep)):]
                )
                
                zip_file.write(absolute_file_path, destination_file_path)