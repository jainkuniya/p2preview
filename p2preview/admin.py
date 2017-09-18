# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Person, Student, Instrutor, Course, RegisteredCourses

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

admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Instrutor, InstrutorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(RegisteredCourses, RegisteredCoursesAdmin)
