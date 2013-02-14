from django.conf.urls.defaults import patterns, include
from tastypie.api import Api

from forge.resources.card import CardResource
from forge.resources.card_set import CardSetResource
from forge.resources.card_type import CardTypeResource
from forge.resources.complete import CompleteResource


v1_api = Api(api_name='v1')
v1_api.register(CardResource())
v1_api.register(CardSetResource())
v1_api.register(CardTypeResource())
v1_api.register(CompleteResource())

urlpatterns = patterns(
    '',
    (r'^$', 'forge.views.index'),
    (r'^api/', include(v1_api.urls)),
)
