# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, render_to_response
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from p2preview.models import Person, Student, Instrutor, Course, RegisteredCourses, GroupDetail, Group

import string
import random

@require_http_methods(["GET"])
@csrf_exempt
def fetch_self(request):
    person = validatePerson(request.META['HTTP_TOKEN'])
    if person != -1:
        if person[0].personType == 1:
            instrutor = Instrutor.objects.filter(iId=person[0])
            data = {
                'success': 1,
                'message': '',
                'self': {
                    'name': person[0].name,
                    'email': person[0].email,
                }
            }
        elif person[0].personType == 2:
            student = Student.objects.filter(sId=person[0])
            data = {
                'success': 1,
                'message': '',
                'self': {
                    'name': person[0].name,
                    'email': person[0].email,
                    'rollNo': student[0].rollNo,
                    'branch': student[0].branch,
                }
            }
    else:
        data = {
            'success': -99,
            'message': 'Please login again',
        }
    return JsonResponse(data, safe=True)


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
    instrutor = validateInstructor(request.META['HTTP_TOKEN'])
    if (instrutor != -1):
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
    else:
        data = {
            'success': -99,
            'message': 'Please login again',
        }
    return JsonResponse(data, safe=True)


@csrf_exempt
def course(request):
    instrutor = validateInstructor(request.COOKIES.get('token'))
    if (instrutor != -1):
        template = loader.get_template('p2preview/course.html')
        courses = getInstructorCourses(instrutor).order_by('-pk')
        courseDetails = []
        for course in courses:
            courseDetails.append({
                'course': course,
                'students': getStudentsInCourse(course),
            })
        context = {
            'courses': courseDetails
        }
        return render_to_response('p2preview/course.html', context)
    else:
        redirectToLogin();

@require_http_methods(["GET"])
@csrf_exempt
def get_student_courses(request):
    student = validateStudent(request.META['HTTP_TOKEN'])
    if (student != -1):
        registeredCourses = RegisteredCourses.objects.filter(sId=student).order_by('-pk')
        courses = []
        for reg in  registeredCourses:
            courses.append({
                'name': reg.courseId.name,
                'code': reg.courseId.code,
                'description': reg.courseId.description,
                'instructorName': reg.courseId.instructorId.iId.name
                })
        data = {
            'success': 1,
            'courses': courses
        }
    else:
        data = {
            'success': -99,
            'message': 'Please login again',
            'courses': []
        }
    return JsonResponse(data, safe=True)

@require_http_methods(["GET"])
@csrf_exempt
def get_student_groups(request):
    student = validateStudent(request.META['HTTP_TOKEN'])
    if (student != -1):
        groupDetails = GroupDetail.objects.filter(sId=student).order_by('-pk')
        groups = []
        for group in groupDetails:
            groups.append({
                'members': get_group_members(group.groupId),
                'name': group.groupId.name,
                'id': group.groupId.pk,
                })
        data = {
            'success': 1,
            'data': {
                'groups': groups
            }
        }
    else:
        data = {
            'success': -99,
            'message': 'Please login again',
            'data': {}
        }
    return JsonResponse(data, safe=True)

@require_http_methods(["POST"])
@csrf_exempt
def add_student_course(request):
    student = validateStudent(request.META['HTTP_TOKEN'])
    if (student != -1):
        registeredCourse = addStudentInCourse(student[0], request.POST['code'])
        if (registeredCourse == -1):
            data = {
                'success': -1,
                'message': 'Please enter a valid code',
                'course': []
            }
        else:
            course = validateCourse(request.POST['code'])
            coursesResponse = []
            coursesResponse.append({
                'name': course[0].name,
                'code': course[0].code,
                'description': course[0].description,
                'instructorName': course[0].instructorId.iId.name
            })
            data = {
                'success': 1,
                'message': 'Course successfully added',
                'course': coursesResponse
            }
    else:
        data = {
            'success': -99,
            'message': 'Please login again',
            'course': []
        }
    return JsonResponse(data, safe=True)

@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    person = Person(name=request.POST['name'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    personType=request.POST['personType'])
    try:
        person.save()
        if request.POST['personType'] == 1:
            instrutor = Instrutor(iId=person,
                                  department=request.POST['department'],
                                  office=request.POST['office'],
                                  visitingHours=request.POST['visitingHours'])
            instrutor.save()
        elif request.POST['personType'] == 2:
            student = Student(sId=person,
                              rollNo=request.POST['rollNo'],
                              branch=request.POST['branch'])
            student.save()
        data = {
            'success': 1,
            'message': 'Successfully registered',
        }
    except:
        """Check if email already registered"""
        persons = Person.objects.filter(email=request.POST['email'])
        if (persons.count() > 0):
            message = request.POST['email'] +  ' is already associated with another account.'
        else:
            message = 'Please try again'
        data = {
            'success': 0,
            'message': message,
        }
    return JsonResponse(data, safe=True)

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

@require_http_methods(["POST"])
@csrf_exempt
def verify_student(request):
    person = validatePerson(request.META['HTTP_TOKEN'])
    if (person != -1):
        student = get_student_from_email(request.POST['email'])
        if (student == -1):
            data = {
                'success': 0,
                'message': "No student is associated with this email ID."
            }
        elif (student == -2):
            data = {
                'success': 0,
                'message': "This email ID is not registered with our system."
            }
        else:
            data = {
                'success': 1,
                'message': "Student is valid",
                'data': {
                    'student': student
                }
            }
    else:
        date = {
            'success': -99,
            'message': "Please login again",
        }
    return JsonResponse(data, safe=True)

def get_student_from_email(email):
    persons = Person.objects.filter(personType=2, email=email)
    if (persons.count() == 1):
        students = Student.objects.filter(sId=persons[0])
        if (students.count() == 1):
            return {
                'name': persons[0].name,
                'email': persons[0].email,
                'rollNo': students[0].rollNo,
            }
        else:
            return -1
    else:
        return -2



@require_http_methods(["POST"])
@csrf_exempt
def create_student_group(request):
    person = validatePerson(request.META['HTTP_TOKEN'])
    if (person != -1):
        group = Group(name="")
        try:
            group.save()
            emails = request.POST['emails'].split(',')
            for email in emails:
                student = get_student_from_email(email)
                if (student != -1):
                    sId = Student.objects.filter(rollNo=student['rollNo'])
                    groupDetail = GroupDetail(groupId=group, sId=sId[0])
                    groupDetail.save()
        except:
            data = {}
        data = {
            'success': 1,
            'message': 'Group successfully created',
            'data': {
                'groups': [{
                    'members': get_group_members(group),
                    'name': group.name,
                    'id': group.pk
                }]
            }
        }
    else:
        date = {
            'success': -99,
            'message': "Please login again",
        }
    return JsonResponse(data, safe=True)

def get_group_members(group):
    groupDetail = GroupDetail.objects.filter(groupId=group)
    members = []
    for member in groupDetail:
        members.append({
            'name': member.sId.sId.name,
            'email': member.sId.sId.email,
            'rollNo': member.sId.rollNo,
        })
    return members

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

def validateStudent(token):
    person = validatePerson(token)
    if person == -1:
        return -1
    students = Student.objects.filter(sId=person)
    if (students.count() == 1):
        return students
    else:
        return -1

def validateCourse(code):
    courses = Course.objects.filter(code=code)
    if (courses.count() == 1):
        return courses
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

def addStudentInCourse(student, courseCode):
    course = validateCourse(courseCode)
    if (course == -1):
        return -1
    else:
        """Check if already registered"""
        registeredCourse = RegisteredCourses.objects.filter(courseId=course[0], sId=student)
        if (registeredCourse.count() == 1):
            return registeredCourse[0]
        try:
            registeredCourse = RegisteredCourses(courseId=course[0], sId=student)
            registeredCourse.save()
            return registeredCourse
        except:
            return -1
