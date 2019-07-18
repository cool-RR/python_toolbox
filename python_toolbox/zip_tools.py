# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Various zip-related tools.'''


import zipfile as zip_module
import io
import os
import re
import pathlib

import fnmatch


def zip_folder(source_folder, zip_path, ignored_patterns=()):
    '''
    Zip `folder` into a zip file specified by `zip_path`.

    Note: Creates a folder inside the zip with the same name of the original
    folder, in contrast to other implementation which put all of the files on
    the root level of the zip.

    `ignored_patterns` are fnmatch-style patterns specifiying file-paths to
    ignore.

    Any empty sub-folders will be ignored.
    '''
    zip_path = pathlib.Path(zip_path)
    source_folder = pathlib.Path(source_folder).absolute()
    assert source_folder.is_dir()

    ignored_re_patterns = [re.compile(fnmatch.translate(ignored_pattern)) for
                           ignored_pattern in ignored_patterns]

    zip_name = zip_path.stem

    internal_pure_path = pathlib.PurePath(source_folder.name)

    with zip_module.ZipFile(str(zip_path), 'w', zip_module.ZIP_DEFLATED) \
                                                                   as zip_file:

        for root, subfolders, files in os.walk(str(source_folder)):
            root = pathlib.Path(root)
            subfolders = map(pathlib.Path, subfolders)
            files = map(pathlib.Path, files)

            for file_path in files:

                if any(ignored_re_pattern.match(root / file_path)
                                for ignored_re_pattern in ignored_re_patterns):
                    continue

                absolute_file_path = root / file_path

                destination_file_path = internal_pure_path / \
                                                        absolute_file_path.name

                zip_file.write(str(absolute_file_path),
                               str(destination_file_path))


def zip_in_memory(files):
    '''
    Zip files in memory and return zip archive as a string.

    Files should be given as tuples of `(file_path, file_contents)`.
    '''
    zip_stream = io.BytesIO()
    with zip_module.ZipFile(zip_stream, mode='w',
                            compression=zip_module.ZIP_DEFLATED) as zip_file:
        assert isinstance(zip_file, zip_module.ZipFile)
        for file_name, file_data in files:
            zip_file.writestr(file_name, file_data)

    return zip_stream.getvalue()

def unzip_in_memory(zip_archive):
    '''
    Unzip a zip archive given as string, returning files

    Files are returned as tuples of `(file_path, file_contents)`.
    '''
    zip_stream = io.BytesIO(zip_archive)
    with zip_module.ZipFile(zip_stream, mode='r',
                            compression=zip_module.ZIP_DEFLATED) as zip_file:
        assert isinstance(zip_file, zip_module.ZipFile)
        return tuple((file_name, zip_file.read(file_name)) for file_name in
                     zip_file.namelist())




