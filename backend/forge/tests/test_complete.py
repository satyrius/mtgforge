from django.http import HttpResponse
from django.test import TestCase
from mock import patch

from forge.resources.complete import CompleteResource
from forge.tests.base import get_uri


class CompleteTest(TestCase):
    @patch.object(CompleteResource, 'create_response')
    def test_cache(self, create_response):
        create_response.return_value = HttpResponse('a')
        res = CompleteResource()

        # The create_response method is called for first call
        r = self.client.get(get_uri(res, q='z'))
        self.assertEqual(create_response.call_count, 1)
        self.assertEqual(r.content, 'a')

        # Next time cached result should be returned
        r = self.client.get(get_uri(res, q='z'))
        self.assertEqual(create_response.call_count, 1)
        self.assertEqual(r.content, 'a')

        # New get parameters will cause resource to create new response
        create_response.return_value = HttpResponse('b')
        r = self.client.get(get_uri(res, q='zy'))
        self.assertEqual(create_response.call_count, 2)
        self.assertEqual(r.content, 'b')
