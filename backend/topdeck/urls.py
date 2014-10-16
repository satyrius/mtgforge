from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from forge import urls as forge_urls


admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^', include(forge_urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
)

# Serve compiled client application directly from static for DEV.
# The nginx should be configured proper to handle / on production.
if settings.DEBUG:
    urlpatterns += patterns(
        'django.contrib.staticfiles.views',
        url(r'^(?:index.html)?$', 'serve', kwargs={'path': 'index.html'}),
        url(r'^(?P<path>(?:js|css|img|fonts)/.*)$', 'serve'),
    )

# Static files
urlpatterns += staticfiles_urlpatterns()

# Uploaded media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
