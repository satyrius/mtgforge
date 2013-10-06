from django.core.cache import get_cache
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(CACHES={
    'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'},
    'provider_page': {'BACKEND': 'crawler.providers.cache.PageCache'},
})
class ProviderTest(TestCase):
    def setUp(self):
        # Invalidate pages cache
        get_cache('provider_page').clear()
