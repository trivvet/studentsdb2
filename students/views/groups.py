# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Groups List
def groups_list(request):
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
    return render(request, 'students/groups.html', {'groups': groups})

# Add Form
  
def groups_add(request):
    return HttpResponse('<h1>Groups Add Form</h1>')

# Edit Form
  
def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

# Delete Page
  
def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
