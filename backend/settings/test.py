import os
import shutil
from settings.common import *

DEBUG_SERP = True

# Save upload media to the temporary directory
MEDIA_ROOT = '/tmp/mtgforge/media/'
# Make it clean before running
if os.path.exists(MEDIA_ROOT):
    shutil.rmtree(MEDIA_ROOT)
for d in ['art', 'thumbs']:
    d = os.path.join(MEDIA_ROOT, d)
    os.makedirs(d)

# Local memory cache is fast enough and it invalidetes when script terminates
CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
}

from settings.local import *