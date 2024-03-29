from forge.resources.base import ModelResource
from oracle.models import CardSet


class CardSetResource(ModelResource):
    class Meta:
        resource_name = 'card_sets'
        limit = 0
        queryset = CardSet.objects.filter(is_published=True)
        allowed_methods = ['get']
