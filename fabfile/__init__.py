import sys
from fabric.api import env
from fabfile.deploy import *
from fabfile.media import *
from fabfile.pg import *


IS_MACOS = sys.platform.startswith('darwin')

env['database'] = 'mtgforge'
env['downloads'] = IS_MACOS and '~/Downloads' or '/tmp'
