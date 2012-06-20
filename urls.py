from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from forge import urls as forge_urls


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mtgforge.views.home', name='home'),

    url(r'^', include(forge_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
