# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from ..models.students import Student
from ..models.groups import Group
from ..models.exams import Exam

def exams_list(request):
    addition = {}
    groups_all = Group.objects.all().order_by('title')
    exams = Exam.objects.all()

    # exams ordering
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('id', 'name', 'date', 'teacher_name', 'exam_group__title'):
        exams = exams.order_by(order_by)
        if reverse == '1':
            exams = exams.reverse()
    else:
        exams = exams.order_by('date')

    # groups paginator
    if exams.count() > 0:
        number = 3
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        exams_count = exams.count()
        if exams_count > number:
            addition = {'has_other_pages': True}
            num_pages = exams_count / number
            page_range = []
            if exams_count % number > 0:
                num_pages += 1
            for i in range(1, num_pages+1):
                page_range.append(i)
            addition['page_range'] = page_range

        if page > 0 and page < num_pages:
            exams = exams[number*(page-1):number*page]
            addition['page'] = page
        else:
            exams = exams[number*(num_pages-1):exams_count]
            addition['page'] = num_pages
    else:
        addition = {}
  
    return render(request, 'students/exams.html', {'exams': exams,
        'groups_all': groups_all, 'addition': addition})

# Add Form

def exams_add(request):
    return HttpResponse('<h1>Exams Add Form</h1>')

# Edit Form
  
def exams_edit(request, eid):
    return HttpResponse('<h1>Edit Exam %s</h1>' % eid)

# Delete Page
  
def exams_delete(request, eid):
    return HttpResponse('<h1>Delete Exam %s</h1>' % eid)
