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
    url(r'^criteria/$', views.criteria_page),
    url(r'^rubricTemplate/$', views.rubric_template),
    url(r'^statistics/$', views.statistics_page),
    url(r'^activity/$', views.activity),
    url(r'^activity/(?P<pk>[0-9]+)/$', views.activity_details),
]
