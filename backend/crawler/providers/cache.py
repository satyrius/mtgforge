from django.core.cache.backends.base import BaseCache
from crawler.models import DataProviderPage


class PageCache(BaseCache):
    def __init__(self, _, params):
        BaseCache.__init__(self, params)

    def make_key(self, key, version=None):
        """Create complex key to get or set cache value

        Argumets:
            key -- Page instance
            version -- For capability with cache interface. Does not maters.
        """
        page = key
        url_hash = page.get_url_hash()
        class_name = page.__class__.__name__
        return dict(url_hash=url_hash, class_name=class_name)

    def get(self, key, default=None, version=None):
        try:
            key = self.make_key(key)
            entry = DataProviderPage.objects.get(**key)
            return entry.name, entry.content, entry.state
        except DataProviderPage.DoesNotExist:
            return None, default, 0

    def set(self, key, value, timeout=None, version=None):
        self.delete(key, version)
        page = key
        key = self.make_key(key)
        DataProviderPage.objects.create(
            url=page.url, name=page.name, state=page.state,
            provider=page.get_provider(), content=value, **key)

    def delete(self, key, version=None):
        key = self.make_key(key)
        DataProviderPage.objects.filter(**key).delete()

    def clear(self):
        DataProviderPage.objects.all().delete()
