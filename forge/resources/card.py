from tastypie.resources import ModelResource
from oracle.models import CardL10n


class CardResource(ModelResource):
    class Meta:
        resource_name = 'card'
        queryset = CardL10n.objects.all()
        allowed_methods = ['get']
