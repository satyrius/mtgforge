from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from forge import urls as forge_urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(forge_urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Static files
urlpatterns += staticfiles_urlpatterns()

# Uploaded media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
