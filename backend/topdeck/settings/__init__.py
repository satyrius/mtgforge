import sys

if 'test' in sys.argv:
    from .test import *
elif sys.platform.startswith('darwin'):
    from .dev import *
else:
    from .prod import *
