# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox import zip_tools


def test_zipping_in_memory():
    ''' '''
    files = (
        ('meow.txt', b"I'm a cat."), 
        ('dog.txt', b"I'm a dog."), 
        ('folder/binary.bin', bytes(bytearray(range(256))))
    )
    
    zip_archive = zip_tools.zip_in_memory(files)
    assert isinstance(zip_archive, bytes)
    assert set(zip_tools.unzip_in_memory(zip_archive)) == set(files)
    