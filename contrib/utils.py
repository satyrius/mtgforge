import datetime
import logging
from hashlib import sha1

from django.conf import settings
from django.core.cache import cache as _djcache
from django.utils import translation
from django.utils.functional import wraps


def translation_aware(func):
    def wrapper(self, *args, **kwargs):
        translation.activate(settings.MODELTRANSLATION_DEFAULT_LANGUAGE)
        func(self, *args, **kwargs)
        translation.deactivate()
    return wrapper


def cache(f, seconds = 900):
    """
        Cache the result of a function call for the specified number of seconds,
        using Django's caching mechanism.
        Assumes that the function never returns None (as the cache returns None to indicate a miss), and that the function's result only depends on its parameters.
        Note that the ordering of parameters is important. e.g. myFunction(x = 1, y = 2), myFunction(y = 2, x = 1), and myFunction(1,2) will each be cached separately.

        http://djangosnippets.org/snippets/564/

        Usage:

        @cache(600)
        def myExpensiveMethod(parm1, parm2, parm3):
            ....
            return expensiveResult
    """
    def wrapper(*args, **kwargs):
        key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest()
        result = _djcache.get(key)
        if result is None:
            result = f(*args, **kwargs)
            _djcache.set(key, result, seconds)
        return result
    return wrapper


def cache_method_calls(func):
    """Cache methods' calls. Store cached results as objects attributes"""
    def wrapper(self, *args, **kwargs):
        key = sha1(str(func.__name__) + str(args) + str(kwargs)).hexdigest()
        if hasattr(self, key):
            return getattr(self, key)
        result = func(self, *args, **kwargs)
        setattr(self, key, result)
        return result
    return wrapper


console_logger = logging.getLogger('stdout')

def measureit(func=None, logger=None):
    if not logger:
        logger = console_logger
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            started_at = datetime.datetime.now()
            result =  func(*args, **kwargs)
            delta = (datetime.datetime.now() - started_at).total_seconds()
            message = u'`{}` has taken {:.2f} sec'.format(name, delta)
            logger.debug(message)
            return result
        return wrapper
    return func and decorator(func) or decorator
