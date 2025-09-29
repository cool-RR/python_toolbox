from __future__ import annotations

import pathlib
import os
import socket
import sys
import re
import urllib.parse
from typing import Iterable

# Constants for CLI
QUOTE_AUTO = 'auto'
QUOTE_NEVER = 'never'
QUOTE_ALWAYS = 'always'

SEPARATOR_NEWLINE = 'newline'
SEPARATOR_SPACE = 'space'

unc_drive_pattern = re.compile(r'^\\\\(?P<host>[^\\]+)\\(?P<share>[^\\])$')


def format_envvar(x: str) -> str:
    return '~' if x == 'HOME' else f'${x}'


def _posh(path_string: str = None, allow_cwd: bool = True) -> str:
    # Return URLs (like http://) unaltered
    if re.match(r'^[a-zA-Z]+://', path_string):
        return path_string

    path = pathlib.Path(path_string)
    if not path.is_absolute():
        if allow_cwd:
            path = pathlib.Path.cwd() / path
        else:
            return pathlib.Path(os.path.normpath(path)).as_posix()
    path = pathlib.Path(os.path.normpath(path))

    if ((sys.platform == 'win32') and
        (unc_drive_match := unc_drive_pattern.fullmatch(str(path.drive))) and
        (unc_drive_match.group('host').lower() == socket.gethostname().lower())):

        share = unc_drive_match.group('share')
        path = pathlib.Path(f'{share}:\\', *path.parts[1:])


    # Define hardcoded paths for some envvars
    envvar_paths = {
        'DXRV': [],
        'DXR': [],
        'VP': [], 
        'DX': [],
        'PF': [],
        'PF8': [],
        'SU': [],
        'RS': [],
        'RG': [],
        'T0V': [],
        'H0V': [],
        'M0V': [
            r'\\VBoxSvr\ROOT\home\ramrachum\.viola',
            r'\\melfi\melfi\home\ramrachum\.viola',
        ],
        'L0V': [r'L:\Users\Administrator\.viola'],
        'W0V': [],
        'R0V': [],
        'N0V': [],
        'T0': [],
        'H0': [],
        'M0': [
            r'\\VBoxSvr\ROOT\home\ramrachum',
            r'\\melfi\melfi\home\ramrachum',
        ],
        'L0': [r'L:\Users\Administrator'],
        'W0': [],
        'R0': [],
        'N0': [],
        'HOME': [],
    }

    # Add environment values if they exist
    for envvar_name in envvar_paths:
        try:
            envvar_value = os.environ[envvar_name]
            envvar_paths[envvar_name].append(pathlib.Path(envvar_value))
        except KeyError:
            pass

    # Try each envvar and its paths
    for envvar_name, paths in envvar_paths.items():
        for envvar_path in paths:
            if path == envvar_path:
                return f'{format_envvar(envvar_name)}'
            try:
                relative_path = path.relative_to(envvar_path)
                return f'{format_envvar(envvar_name)}/{relative_path.as_posix()}'
            except ValueError:
                continue

    return path.as_posix()


def posh(path_strings: Iterable[str] | str | None = None,
         quote_mode: str = QUOTE_AUTO,
         separator: str = SEPARATOR_NEWLINE,
         allow_cwd: bool = True) -> str:
    """
    Convert paths to a more readable format using environment variables.

    Args:
        paths: A single path or list of paths to process
        quote_mode: Whether to quote paths (QUOTE_AUTO, QUOTE_NEVER, or QUOTE_ALWAYS)
        separator: Separator to use between multiple paths (SEPARATOR_NEWLINE or SEPARATOR_SPACE)
        allow_cwd: When False, don't resolve relative paths against current working directory

    Returns:
        Formatted path string(s)
    """
    if path_strings is None:
        return ""

    if not isinstance(path_strings, (list, tuple)):
        path_strings = [path_strings]

    results = [_posh(path_string, allow_cwd=allow_cwd) for path_string in path_strings]

    if quote_mode == QUOTE_ALWAYS:
        quoted_results = [f'"{result}"' for result in results]
    elif quote_mode == QUOTE_AUTO:
        if separator == SEPARATOR_SPACE and len(results) > 1:
            # If using space separator with multiple paths, quote all paths in auto mode
            quoted_results = [f'"{result}"' for result in results]
        else:
            quoted_results = [f'"{result}"' if ' ' in result else result for result in results]
    else:
        assert quote_mode == QUOTE_NEVER
        quoted_results = results

    sep = '\n' if separator == SEPARATOR_NEWLINE else ' '
    return sep.join(quoted_results)


def ensure_windows_path_string(path_string: str) -> str:
    # Handle file:/// URLs
    if path_string.startswith('file:///'):
        # Strip the file:/// prefix and decode URL encoding
        return urllib.parse.unquote(path_string[8:])

    # Return other URLs (like http://) unaltered
    if re.match(r'^[a-zA-Z]+://', path_string):
        return path_string

    path = pathlib.Path(path_string)
    posix_path = path.as_posix()
    if re.match('^/[a-zA-Z]/.*$', posix_path):
        # Handle local drive paths like /c/Users/...
        return '%s:%s' % (
            posix_path[1],
            re.sub('(?<=[^\\\\])\\\\ ', ' ', posix_path).replace('/', '\\')[2:]
        )
    elif re.match('^//[^/]+/.*$', posix_path):
        # Handle UNC network paths like //server/share/...
        return posix_path.replace('/', '\\')
    else:
        return path_string


def posh_path(path: pathlib.Path | str, allow_cwd: bool = True) -> str:
    """Process a path using the posh function directly."""
    path_str = str(path)
    if sys.platform == 'win32':
        path_str = ensure_windows_path_string(path_str)
    return _posh(path_str, allow_cwd=allow_cwd)

posh('foo')