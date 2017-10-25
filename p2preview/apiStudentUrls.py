from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^courses/', views.get_student_courses),
    url(r'^groups/', views.get_student_groups),
    url(r'^addNewCourse/', views.add_student_course),
    url(r'^create_group/', views.create_student_group),
    url(r'^getActivityGroupComposition/', views.get_activity_group_composition),
    url(r'^registerGroupToActivity/', views.register_group_to_activity),
    url(r'^submitResponses/', views.submit_responses),
    url(r'^activities/', views.student_activities)
]
