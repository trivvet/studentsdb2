# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Groups List
def groups_list(request):
    groups = (
         {'id': 1,
          'name': u'БМ - 1',
          'leader_name': u'Андрій',
          'leader_surname': u'Комисливий'},
         {'id': 2,
          'name': u'БМ - 2',
          'leader_name': u'Павло',
          'leader_surname': u'Очерет'},
         {'id': 3,
          'name': u'БМ - 3',
          'leader_name': u'Олена',
          'leader_surname': u'Денисенко'}
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
