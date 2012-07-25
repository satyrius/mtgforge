import hashlib
from django.core.cache.backends.base import BaseCache
from oracle.models import DataProviderPage


class PageCache(BaseCache):
    def __init__(self, _, params):
        BaseCache.__init__(self, params)

    def make_key(self, key, version=None):
        """Create complex key to get or set cache value

        Argumets:
            key -- ProviderPage instance
            version -- For capability with cache interface. Does not maters.
        """
        page = key
        url_hash = hashlib.sha1(page.url).hexdigest()
        page_name = page.__class__.__name__
        return dict(url_hash=url_hash, name=page_name)

    def get(self, key, default=None, version=None):
        try:
            key = self.make_key(key)
            return DataProviderPage.objects.get(**key).content
        except DataProviderPage.DoesNotExist:
            return default

    def set(self, key, value, timeout=None, version=None):
        page = key
        key = self.make_key(key)
        DataProviderPage.objects.filter(**key).delete()
        DataProviderPage.objects.create(
            url=page.url,
            data_provider=page.get_provider(),
            content=value,
            **key)

    def clear(self):
        DataProviderPage.objects.all().delete()

