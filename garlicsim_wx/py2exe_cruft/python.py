# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import sys
import os.path

arguments = sys.argv[1:]

assert len(arguments) == 1
(code_file_path,) = arguments
assert os.path.isfile(code_file_path)

locals_to_use = {
    '__file__': code_file_path,
    '__name__': '__main__'
}

sys.exit(execfile(code_file_path, globals(), locals_to_use))