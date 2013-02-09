from functools import wraps
from tastypie.resources import ModelResource as TastypieModelResource


class ModelResource(TastypieModelResource):
    pass


def cached_response(func):
    @wraps(func)
    def wrapper(self, request, **kwargs):
        cache = self._meta.cache
        params = {}
        if request and request.GET:
            params.update(request.GET)
        if kwargs:
            params.update(**kwargs)
        cache_key = self.generate_cache_key(
            func.__name__, 'response', **params)

        response = cache.get(cache_key)
        if response is None:
            response = func(self, request, **kwargs)
            cache.set(cache_key, response)

        return response
    return wrapper
