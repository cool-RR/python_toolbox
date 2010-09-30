"""Main entry point"""

import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "unittest2"

__unittest = True

from garlicsim.general_misc.third_party.unittest2.main import main_
main_()
