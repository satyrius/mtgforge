from django.core.cache.backends.base import BaseCache
from oracle.models import DataProviderPage
from oracle.providers import ProviderPage


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
        url_hash = page.get_url_hash()
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
        dp = isinstance(page, ProviderPage) and page.get_provider() or None
        DataProviderPage.objects.create(
            url=page.url, data_provider=dp, content=value, **key)

    def clear(self):
        DataProviderPage.objects.all().delete()

