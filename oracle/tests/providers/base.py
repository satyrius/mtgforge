from django.test import TestCase
from django.test.utils import override_settings


@override_settings(CACHES={
    'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'},
    'provider_page': {'BACKEND': 'oracle.providers.cache.PageCache'},
})
class ProviderTest(TestCase):
    fixtures = ['data_provider']
