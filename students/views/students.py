# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Student List

def students_list(request):
#  import pdb;pdb.set_trace()
    students = (
        {'id': 1,
         'first_name': u'Вадим',
         'last_name': u'Афанасьєв',
         'ticket': 22,
         'image': 'img/1.jpeg'},
         {'id': 2,
         'first_name': u'Олег',
         'last_name': u'Обліховський',
         'ticket': 108,
         'image': 'img/2.jpeg'},
         {'id': 3,
         'first_name': u'Анна',
         'last_name': u'Григоренко',
         'ticket': 67,
         'image': 'img/3.jpeg'}
    )
    groups = (
         {'id': 1,
          'name': u'БМ - 1',
          'leader': {'first_name': u'Андрій', 'last_name': u'Комисливий', 
                    'id': 4}},
         {'id': 2,
          'name': u'БМ - 2',
          'leader': {'first_name': u'Павло', 'last_name': u'Очерет', 
                    'id': 5}},
         {'id': 3,
          'name': u'БМ - 3',
          'leader': {'first_name': u'Олена', 'last_name': u'Доровська', 
                    'id': 6}},
    )
    return render(request, 'students/students_list.html', 
        {'students': students, 'groups': groups})

# Add Form

def students_add(request):
    return HttpResponse('<h1>Students Add Form</h1>')

# Edit Form

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

# Delete Page
  
def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
