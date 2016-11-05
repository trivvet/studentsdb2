# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students

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
          'leader_name': u'Андрій',
          'leader_surname': u'Комисливий'},
         {'id': 2,
          'name': u'БМ - 2',
          'leader_name': u'Павло',
          'leader_surname': u'Очерет'},
    )
    return render(request, 'students/students_list.html', 
        {'students': students, 'groups': groups})
  
def students_add(request):
    return HttpResponse('<h1>Students Add Form</h1>')
  
def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)
  
def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
  
# Views for Groups

def groups_list(request):
    return HttpResponse('<h1>Group Listing</h1>')
  
def groups_add(request):
    return HttpResponse('<h1>Groups Add Form</h1>')
  
def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)
  
def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
  
# View for Journal

def journal_list(request):
    return HttpResponse('<h1>Journal List</h1>')


# Create your views here.
