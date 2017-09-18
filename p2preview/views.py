# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, render_to_response
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from p2preview.models import Person, Student, Instrutor, Course, RegisteredCourses

import string
import random

# Create your views here.
@csrf_exempt
def home(request):
    person = validatePerson(request.COOKIES.get('token'))
    if person != -1:
        template = loader.get_template('p2preview/home.html')
        context = {
            'person_name': person[0].name,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirectToLogin()

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
    instrutor = validateInstructor(request.COOKIES.get('token'))
    if (instrutor != -1):
        template = loader.get_template('p2preview/course.html')
        courses = getInstructorCourses(instrutor)
        courseDetails = []
        for course in courses:
            print course.name
            courseDetails.append({
                'course': course,
                'students': getStudentsInCourse(course),
                'count': getStudentsInCourse(course).count()
            })
        print courseDetails
        context = {
            'courses': courseDetails
        }
        return render_to_response('p2preview/course.html', context)
    else:
        redirectToLogin();

@csrf_exempt
def new_course_page(request):
    return render(request, 'p2preview/course_new.html')

def rubric_template(request):
    return render(request, 'p2preview/rubric_template.html')

def signUp_page(request):
    return render(request, 'p2preview/signup.html')

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

@csrf_exempt
def logout(request):
    person = validatePerson(request.META['HTTP_TOKEN'])
    if (person != -1):
        person.update(token='')
    data = {
        'success': 1,
        'message': "Successfully logged off"
    }
    return JsonResponse(data, safe=True)

def validatePerson(token):
    if token != '':
        person = Person.objects.filter(token=token)
        if (person.count() == 1):
            return person
        else:
            return -1
    else:
        return -1

def validateInstructor(token):
    person = validatePerson(token)
    if person == -1:
        return -1
    instrutors = Instrutor.objects.filter(iId=person)
    if (instrutors.count() == 1):
        return instrutors
    else:
        return -1

def getRandomString(length):
    char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.sample(char_set*length, length))

def redirectToLogin():
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('token')
    return response

def getInstructorCourses(iId):
    return Course.objects.filter(instructorId=iId)

def getStudentsInCourse(cId):
    return RegisteredCourses.objects.filter(courseId=cId)
