from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    'django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
)
