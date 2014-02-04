# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import monkeypatching_tools

try:
    import pathlib

except ImportError:
    pass

else:
    
    @monkeypatching_tools.monkeypatch(pathlib.Path, override_if_exists=False)
    def read_bytes(self):
        """
        Open the file in bytes mode, read it, and close the file.
        """
        with self.open(mode='rb') as f:
            return f.read()

    @monkeypatching_tools.monkeypatch(pathlib.Path, override_if_exists=False)
    def read_text(self, encoding=None, errors=None, newline=None):
        """
        Open the file in text mode, read it, and close the file.
        """
        with self.open(mode='r', encoding=encoding,
                       errors=errors, newline=newline) as f:
            return f.read()

    @monkeypatching_tools.monkeypatch(pathlib.Path, override_if_exists=False)
    def write_bytes(self, data, append=False, exclusive=False):
        """
        Open the file in bytes mode, write to it, and close the file.
        """
        if append and exclusive:
            raise TypeError('write_bytes does not accept both '
                            '"append" and "exclusive" mode.')
        mode = 'ab' if append else 'xb' if exclusive else 'wb'
        with self.open(mode=mode) as f:
            return f.write(data)

    @monkeypatching_tools.monkeypatch(pathlib.Path, override_if_exists=False)
    def write_text(self, data, encoding=None, errors=None,
                   newline=None, append=False, exclusive=False):
        """
        Open the file in text mode, write to it, and close the file.
        """
        if append and exclusive:
            raise TypeError('write_text does not accept both '
                            '"append" and "exclusive" mode.')
        mode = 'a' if append else 'x' if exclusive else 'w'
        with self.open(mode=mode, encoding=encoding,
                       errors=errors, newline=newline) as f:
            return f.write(data)
    