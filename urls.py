from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mtgforge.views.home', name='home'),
    # url(r'^mtgforge/', include('mtgforge.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
