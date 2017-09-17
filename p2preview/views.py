# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from p2preview.models import Person, Student, Instrutor, Course

import string
import random

# Create your views here.
@csrf_exempt
def home(request):
    token = request.COOKIES.get('token')
    person = Person.objects.filter(token=token)
    if person.count() == 1:
        return render(request, 'p2preview/home.html')
    elif person.count() == 0:
        return HttpResponseRedirect('login/')
    else:
        response = HttpResponseRedirect('login/')
        response.delete_cookie('token')
        return response

@csrf_exempt
def login_page(request):
    token = request.COOKIES.get('token')
    person = Person.objects.filter(token=token)
    if person.count() == 1:
        return HttpResponseRedirect('/')
    elif person.count() == 0:
        return render(request, 'p2preview/login.html')
    else:
        return redirectToLogin()

@require_http_methods(["POST"])
@csrf_exempt
def create_course(request):
    person = validatePerson(request.META['HTTP_TOKEN'])
    if (person != -1):
        instrutor = Instrutor.objects.filter(iId=person)
        if instrutor.count() == 1:
            course = Course(name=request.POST['name'],
                            description=request.POST['description'],
                            instructorId=instrutor[0],
                            code=getRandomString(5))
            try:
                course.save()
                data = {
                    'success': 1,
                    'message': 'Course Successfully Created',
                }
            except:
                data = {
                    'success': 0,
                    'message': 'Please try again',
                }
            return JsonResponse(data, safe=True)
        else:
            return redirectToLogin()
    else:
        return redirectToLogin()


@csrf_exempt
def course(request):
    return render(request, 'p2preview/course.html')

@csrf_exempt
def new_course_page(request):
    return render(request, 'p2preview/course_new.html')

def rubric_template(request):
    return render(request, 'p2preview/rubric_template.html')

@csrf_exempt
def login(request):
    """
    Check crendentials
    """
    if request.method == 'POST':
        person = Person.objects.filter(email=request.POST['email'], password=request.POST['password'])
        if (person.count() == 1):
            char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
            token = ''.join(random.sample(char_set*10, 10))
            person.update(token=token)
            data = {
                'success': 1,
                'token': token,
                'message': 'Successfully logged In'
            }
        elif (person.count() > 1):
            data = {
                'success': 0,
                'message': 'Multiple accounts are associated with this email id. Please contact administrator'
            }
        elif (person.count() == 0):
            person = Person.objects.filter(email=request.POST['email'])
            if (person.count() == 1):
                data = {
                    'success': 0,
                    'message': 'Hi, ' + person[0].name + ' your password is wrong. Please try again'
                }
            elif (person.count() == 0):
                data = {
                    'success': 0,
                    'message': "Sorry, this email address isn't registered with us."
                }
            elif (person.count() > 1):
                data = {
                    'success': 0,
                    'message': "Multiple accounts are associated with this email id. Please contact administrator"
                }

        return JsonResponse(data, safe=True)

def validatePerson(token):
    person = Person.objects.filter(token=token)
    if (person.count() == 1):
        return person
    else:
        return -1

def getRandomString(length):
    char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.sample(char_set*length, length))

def redirectToLogin():
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('token')
    return response
