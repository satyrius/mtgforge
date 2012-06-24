from . import ModelResource
from oracle.models import CardType


class CardTypeResource(ModelResource):
    class Meta:
        resource_name = 'card_types'
        queryset = CardType.objects.filter(category=CardType.TYPE)
        allowed_methods = ['get']
