from django.conf.urls.defaults import patterns, include
from tastypie.api import Api
from .resources.card import CardResource

v1_api = Api(api_name='v1')
v1_api.register(CardResource())

urlpatterns = patterns(
    'django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^api/', include(v1_api.urls)),
)
