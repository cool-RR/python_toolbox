from __future__ import annotations

import pathlib
import os
import subprocess
import threading
import atexit

class PoshStreamProcessor:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._process = None
        self._posh_script_path = pathlib.Path(os.path.expandvars('$DX/bin/Common/posh'))
        self._start_process()
        # Register cleanup on exit
        atexit.register(self._cleanup)

    def _start_process(self) -> None:
        """Start the posh process in stream mode."""
        if self._posh_script_path.exists():
            try:
                self._process = subprocess.Popen(
                    ['python', str(self._posh_script_path), '--stream'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1  # Line buffered
                )
            except (subprocess.SubprocessError, FileNotFoundError):
                self._process = None

    def _cleanup(self) -> None:
        """Clean up the process on exit."""
        if self._process and self._process.poll() is None:
            self._process.stdin.close()
            self._process.terminate()
            try:
                self._process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self._process.kill()

    def process_path(self, path: pathlib.Path | str) -> str:
        """Process a single path using the stream mode."""
        path = pathlib.Path(path)

        with self._lock:
            # If process doesn't exist or has died, try to start it
            if not self._process or self._process.poll() is not None:
                self._start_process()

            # If we still don't have a process, fall back to path.as_posix()
            if not self._process:
                return path.as_posix()

            try:
                # Send the path to the process
                self._process.stdin.write(str(path) + '\n')
                self._process.stdin.flush()

                # Read the response
                result = self._process.stdout.readline()
                if result:
                    return result.strip()
                else:
                    # Process might have died
                    self._process = None
                    return path.as_posix()

            except (OSError, IOError):
                # Process communication failed
                self._process = None
                return path.as_posix()

# Create a singleton instance
_posh_processor = PoshStreamProcessor()

def posh_path(path: pathlib.Path | str) -> str:
    """Process a path using the persistent posh stream processor."""
    return _posh_processor.process_path(path)