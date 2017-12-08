# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Person, Student, Instrutor, Course, RegisteredCourses, GroupDetail, Group, Generic, GenericOption, Criteria, Response, Activity, Rubric, RegisteredGroupsForActivity, UploadFile, ActivityAssigment, ActivityImageAssigment

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'password', 'lastLogined', 'personType', 'token']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'sId', 'rollNo', 'branch']

class InstrutorAdmin(admin.ModelAdmin):
    list_display = ['id', 'iId', 'department', 'office', 'visitingHours']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'instructorId', 'name', 'description', 'code']

class RegisteredCoursesAdmin(admin.ModelAdmin):
    list_display = ['courseId', 'sId']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'creationDate', 'name']

class GroupDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'sId', 'groupId']

class RubricAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lastModified', 'iId']

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'courseId', 'rubricId', 'name', 'code', 'duration', 'isActive', 'groupSize', 'textOrImage']

class GenericAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'answer']

class GenericOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'genericId', 'option', 'points', 'optionNo']

class CriteriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'rubricId', 'genericId']

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'registeredGroup', 'criteria', 'response', 'comment']

class RegisteredGroupsForActivityAdmin(admin.ModelAdmin):
    list_display = ['groupId', 'assigmentPk', 'activityId']

class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'file']

class ActivityAssigmentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'text', 'activity', 'groupId', 'count']

class ActivityImageAssigmentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'fileURL', 'activity', 'groupId', 'count']

admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Instrutor, InstrutorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(RegisteredCourses, RegisteredCoursesAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupDetail, GroupDetailAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Generic, GenericAdmin)
admin.site.register(GenericOption, GenericOptionAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(RegisteredGroupsForActivity, RegisteredGroupsForActivityAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(ActivityAssigment, ActivityAssigmentAdmin)
admin.site.register(ActivityImageAssigment, ActivityImageAssigmentAdmin)
