from django.conf import settings
from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from forge import urls as forge_urls


admin.autodiscover()

urlpatterns = patterns('',  # NOQA
    (r'^$', TemplateView.as_view(template_name='index.html')),
    (r'^', include(forge_urls)),
    (r'^admin/grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
)

# Static files
urlpatterns += staticfiles_urlpatterns()

# Uploaded media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
