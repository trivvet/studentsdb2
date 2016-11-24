# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from ..models.students import Student
from ..models.groups import Group
from ..models.exams import Exam
from ..models.results import Result

def results_list(request):
    groups_all = Group.objects.all().order_by('title')
    results = Result.objects.all()
    
    addition = {}
    return render(request, 'students/results.html', {'groups_all': groups_all, 
        'results': results, 'addition': addition})
        
def results_add(request):
    return HttpResponse('<h1>Results Add Form</h1>')

# Edit Form
  
def results_edit(request, rid):
    return HttpResponse('<h1>Edit Result %s</h1>' % rid)

# Delete Page
  
def results_delete(request, rid):
    return HttpResponse('<h1>Delete Result %s</h1>' % rid)
