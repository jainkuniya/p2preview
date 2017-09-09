# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=25, blank=False, default='')
    email = models.EmailField(max_length=20, blank=False, default='', unique=True)
    password = models.CharField(max_length=20, blank=False, default='')
    personType = models.IntegerField(blank=False)
    lastLogined = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=20, blank=True, default='')

class Student(models.Model):
    sId = models.ForeignKey(Person, on_delete=models.CASCADE)
    rollNo = models.CharField(max_length=8, blank=False, default='')
    branch = models.CharField(max_length=5, blank=False, default='')

class Instrutor(models.Model):
    iId = models.ForeignKey(Person, on_delete=models.CASCADE)
    department = models.CharField(max_length=5, blank=False, default='')
    office = models.CharField(max_length=10, blank=False, default='')
    visitingHours = models.CharField(max_length=20, blank=False, default='')

class Course(models.Model):
    name = models.CharField(max_length=15, blank=False, default='')
    instructorId = models.ForeignKey(Instrutor, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, blank=False, default='')

class Rubric(models.Model):
    name = models.CharField(max_length=15, blank=False, default='')
    lastModified = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    rubricId = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, blank=False, default='')
    code = models.CharField(max_length=5, blank=False, default='')
    imageURL = models.URLField(blank=False)
    duration = models.IntegerField(blank=False)
    isActive = models.BooleanField(blank=False, default=False)
    groupSize = models.IntegerField(default=1)

class Groups(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=10, blank=True, default='')

class GroupDetails(models.Model):
    groupId = models.ForeignKey(Groups, on_delete=models.CASCADE)
    sId = models.ForeignKey(Student, on_delete=models.CASCADE)

class Generic(models.Model):
    description = models.CharField(max_length=100, blank=False, default='')
    answer = models.IntegerField()

class GenericOptions(models.Model):
    genericId = models.ForeignKey(Generic, on_delete=models.CASCADE)
    option = models.CharField(max_length=30, blank=False, default='')
    points = models.IntegerField(default=0)

class Criteria(models.Model):
    rubricId = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    genericId = models.ForeignKey(Generic, on_delete=models.CASCADE)

class Response(models.Model):
    groupId = models.ForeignKey(Groups, on_delete=models.CASCADE)
    activityId = models.ForeignKey(Activity, on_delete=models.CASCADE)
    response = models.CharField(max_length=1, blank=False, default='')
    comment = models.CharField(max_length=30, blank=True, default='')
