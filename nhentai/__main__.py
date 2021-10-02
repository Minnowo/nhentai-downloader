

import sys

if __package__ is None and not hasattr(sys, "frozen"):
    import os.path
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.realpath(path))


import nhentai

if __name__ == "__main__":
    sys.exit(nhentai.main())
