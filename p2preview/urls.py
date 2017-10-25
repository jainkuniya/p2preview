from django.conf.urls import include, url

from . import views
from . import apiUrls as api_urls

urlpatterns = [
    url(r'^', include(api_urls.urlpatterns)),
	url(r'^$', views.home),
    url(r'^login/$', views.login_page),
    url(r'^signUp/$', views.signUp_page),
    url(r'^course/$', views.course),
    url(r'^course/new/$', views.new_course_page),
    url(r'^rubricTemplate/$', views.rubric_template),
    url(r'^addActivity/$', views.add_activity),
    url(r'^statistics/$', views.statistics_page),
]
