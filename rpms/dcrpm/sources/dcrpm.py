#!/opt/homebrew/bin/python2.7

import os
import sys
from dcrpm import main

if __name__ == "__main__":
    os.environ["PATH"] = "/opt/yum/bin:{}".format(os.environ["PATH"])
    sys.exit(main.main())
