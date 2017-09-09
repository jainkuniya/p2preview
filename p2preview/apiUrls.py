from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/v1/login/', views.login),
]
