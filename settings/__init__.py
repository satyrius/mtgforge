from .media import MEDIA_BUNDLES
from .cdn import *
from .common import *
from .logging import get_logging_configuration

try:
    from .local import *
except ImportError:
    pass

LOGGING = get_logging_configuration(debug=DEBUG)
