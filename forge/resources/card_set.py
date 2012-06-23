from tastypie.resources import ModelResource
from oracle.models import CardSet


class CardSetResource(ModelResource):
    class Meta:
        resource_name = 'card_set'
        limit = 0
        queryset = CardSet.objects.all()
        allowed_methods = ['get']
