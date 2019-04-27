# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.locking import ReadWriteLock


def test():
    ''' '''
    read_write_lock = ReadWriteLock()
    with read_write_lock.read:
        pass
    with read_write_lock.write:
        pass
    with read_write_lock.read as enter_return_value:
        assert enter_return_value is read_write_lock

    with read_write_lock.read:
        with read_write_lock.read:
            with read_write_lock.read:
                with read_write_lock.read:
                    with read_write_lock.write:
                        with read_write_lock.write:
                            with read_write_lock.write:
                                with read_write_lock.write:
                                    pass

    with read_write_lock.write:
        with read_write_lock.write:
            with read_write_lock.write:
                with read_write_lock.write:
                    with read_write_lock.read:
                        with read_write_lock.read:
                            with read_write_lock.read:
                                with read_write_lock.read:
                                    pass

