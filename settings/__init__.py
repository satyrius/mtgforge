import sys

if 'test' in sys.argv:
    from test import *
else:
    from dev import *
