from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/v1/login/', views.login),
    url(r'^api/v1/logout/', views.logout),
    url(r'^api/v1/create_course/', views.create_course),
]
