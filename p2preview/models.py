# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=45, blank=False, default='')
    email = models.EmailField(blank=False, default='', unique=True)
    password = models.CharField(max_length=20, blank=False, default='')
    personType = models.IntegerField(blank=False)
    lastLogined = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.name

class Student(models.Model):
    sId = models.ForeignKey(Person, on_delete=models.CASCADE)
    rollNo = models.CharField(max_length=8, blank=False, default='')
    branch = models.CharField(max_length=5, blank=False, default='')

    def __str__(self):
        return self.sId.name + " " + self.rollNo

class Instrutor(models.Model):
    iId = models.ForeignKey(Person, on_delete=models.CASCADE)
    department = models.CharField(max_length=5, blank=False, default='')
    office = models.CharField(max_length=10, blank=False, default='')
    visitingHours = models.CharField(max_length=20, blank=False, default='')

    def __str__(self):
        return self.iId.name

class Course(models.Model):
    name = models.TextField(blank=False, default='')
    description = models.TextField(max_length=200, blank='True', default='')
    instructorId = models.ForeignKey(Instrutor, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, blank=False, default='', unique=True)

    def __str__(self):
        return self.name

class RegisteredCourses(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    sId = models.ForeignKey(Student, on_delete=models.CASCADE)

class Rubric(models.Model):
    iId = models.ForeignKey(Instrutor, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False, default='')
    lastModified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    iId = models.ForeignKey(Instrutor, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    rubricId = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    name = models.TextField(blank=False, default='')
    code = models.CharField(max_length=5, blank=False, default='')
    duration = models.IntegerField(blank=False)
    isActive = models.BooleanField(blank=False, default=False)
    groupSize = models.IntegerField(default=1)
    textOrImage = models.BooleanField(blank=False)

    def __str__(self):
        return self.name

class Group(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return self.name

class GroupDetail(models.Model):
    groupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    sId = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('groupId', 'sId')

class Generic(models.Model):
    description = models.CharField(max_length=100, blank=False, default='')
    answer = models.IntegerField(blank=True)
    iId = models.ForeignKey(Instrutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class GenericOption(models.Model):
    genericId = models.ForeignKey(Generic, on_delete=models.CASCADE)
    option = models.TextField(blank=False, default='')
    points = models.IntegerField(default=0)
    optionNo = models.IntegerField(default=0)

    class Meta:
        unique_together = ('genericId', 'optionNo')

class RegisteredGroupsForActivity(models.Model):
    groupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    assigmentPk = models.IntegerField()
    activityId = models.ForeignKey(Activity, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('groupId', 'assigmentPk')

class Criteria(models.Model):
    rubricId = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    genericId = models.ForeignKey(Generic, on_delete=models.CASCADE)

    def __str__(self):
        return self.rubricId.name + " " + self.genericId.description

    class Meta:
        unique_together = ('rubricId', 'genericId')

class Response(models.Model):
    registeredGroup = models.ForeignKey(RegisteredGroupsForActivity, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    response = models.CharField(max_length=1, blank=False, default='')
    comment = models.CharField(max_length=30, blank=True, default='', null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('registeredGroup', 'criteria')

class UploadFile(models.Model):
    file = models.ImageField(upload_to='static/p2preview/files')

class ActivityImageAssigment(models.Model):
    fileURL = models.CharField(max_length=5000, blank=False, default='')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    groupId = models.TextField(blank=True, default='', null=True)
    count = models.IntegerField(default=0, blank=True)

class ActivityAssigment(models.Model):
    text = models.CharField(max_length=5000, blank=False, default='')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    groupId = models.TextField(blank=True, default='', null=True)
    count = models.IntegerField(default=0, blank=True)
