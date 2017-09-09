from django.conf.urls import include, url

from . import views
from . import apiUrls as api_urls

urlpatterns = [
    url(r'^', include(api_urls.urlpatterns)),
	url(r'^$', views.home),
    url(r'^login/', views.login_page),
]
