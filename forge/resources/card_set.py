from . import ModelResource
from oracle.models import CardSet


class CardSetResource(ModelResource):
    class Meta:
        resource_name = 'card_sets'
        limit = 0
        queryset = CardSet.objects.all()
        allowed_methods = ['get']
