from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

from p2preview import urls as p2preview_urls

import p2preview.views

urlpatterns = [
    url(r'^', include(p2preview_urls.urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
