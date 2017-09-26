from django.conf.urls import include, url

from . import views
from . import apiStudentUrls as api_student_urls

urlpatterns = [
    url(r'^api/v1/student/', include(api_student_urls.urlpatterns)),
    url(r'^api/v1/login/', views.login),
    url(r'^api/v1/logout/', views.logout),
    url(r'^api/v1/register/', views.register),
    url(r'^api/v1/create_course/', views.create_course),
]
