import urllib
import urls  # to be able to reverse resource url
from django_any import any_model
from tastypie.test import ResourceTestCase

from forge.management.commands.build_fts_index import Command as BuildIndex
from forge.resources.card import CardResource
from oracle.models import Card, CardFace, CardSet, CardImage, CardRelease


def get_uri(resource, **kwargs):
    uri = resource.get_resource_uri()
    if kwargs:
        uri += '?' + urllib.urlencode(kwargs)
    return uri


class SerpTest(ResourceTestCase):
    def setUp(self):
        super(SerpTest, self).setUp()
        self.uri = CardResource('v1').get_resource_search_uri()

    def build_fts(self):
        BuildIndex().handle(verbosity=0)

    def search(self, build_fts=True, **kwargs):
        if build_fts:
            self.build_fts()
        return self.deserialize(self.api_client.get(self.uri, data=kwargs))

    def create_card(self, **kwargs):
        card = any_model(Card)
        face = any_model(CardFace, card=card, colors=[], **kwargs)
        any_model(CardRelease, card=card, card_set=any_model(CardSet),
                  art=any_model(CardImage))
        return face

    def get_cards(self, serp, field='name'):
        return [cf[field] for cf in serp['objects']]
