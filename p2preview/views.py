# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from p2preview.models import Person, Student, Instrutor

import string
import random

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, 'login.html')

@csrf_exempt
def login(request):
    """
    Check crendentials
    """
    if request.method == 'POST':
        person = Person.objects.filter(email=request.POST['email'], password=request.POST['password'])
        if (person.count() == 1):
            char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
            person.update(token=''.join(random.sample(char_set*10, 10)))
            data = {
                'success': 1,
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
            else:
                data = {
                    'success': 0,
                    'message': 'Multiple accounts are associated with this email id. Please contact administrator'
                }

        return JsonResponse(data, safe=True)
