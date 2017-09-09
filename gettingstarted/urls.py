from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from p2preview import urls as p2preview_urls

import p2preview.views


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^', include(p2preview_urls.urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
]
