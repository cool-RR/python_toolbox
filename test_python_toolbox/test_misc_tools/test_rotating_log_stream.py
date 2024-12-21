# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import pathlib
import tempfile
import shutil
import io
import sys

from python_toolbox.misc_tools import RotatingLogStream


def test_basic():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        log_path = temp_dir / 'test.log'

        stream = RotatingLogStream(log_path)
        stream.write('hello\n')
        stream.write('world\n')

        assert log_path.exists()
        content = log_path.read_text()
        assert 'hello' in content
        assert 'world' in content


def test_rotation():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        log_path = temp_dir / 'test.log'
        old_log_path = log_path.with_suffix('.old')

        # Create a small max size to trigger rotation
        stream = RotatingLogStream(log_path, max_size_in_mb=0.0001) # ~100 bytes

        # Write enough data to trigger rotation
        for i in range(20):
            stream.write('x' * 10 + '\n')

        assert old_log_path.exists()
        assert log_path.exists()

        old_content = old_log_path.read_text()
        new_content = log_path.read_text()
        assert len(old_content) > len(new_content)


def test_with_original_stream():
    string_io = io.StringIO()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        log_path = temp_dir / 'test.log'

        stream = RotatingLogStream(log_path, original_stream=string_io)
        stream.write('test message\n')

        assert string_io.getvalue() == 'test message\n'
        assert 'test message' in log_path.read_text()



def test_install():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        log_path = temp_dir / 'test.log'

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        try:
            RotatingLogStream.install(log_path)

            print('stdout message')
            print('error message', file=sys.stderr)

            assert log_path.exists()
            content = log_path.read_text()
            assert 'stdout message' in content
            assert 'error message' in content

        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

