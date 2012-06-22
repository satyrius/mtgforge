from django.conf.urls.defaults import patterns, include
from tastypie.api import Api
from .resources.card import CardResource
from .resources.card_set import CardSetResource
from .resources.card_type import CardTypeResource


v1_api = Api(api_name='v1')
v1_api.register(CardResource())
v1_api.register(CardSetResource())
v1_api.register(CardTypeResource())

urlpatterns = patterns(
    'django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^api/', include(v1_api.urls)),
)
