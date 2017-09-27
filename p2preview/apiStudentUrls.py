from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^courses/', views.get_student_courses),
    url(r'^addNewCourse/', views.add_student_course),
]
