# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from .students import Student, Group

# Groups List
def groups_list(request):
    groups = Group.objects.all()
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('title', 'leader__last_name', 'id'):
        groups = groups.order_by(order_by)
        if reverse == '1':
            groups = groups.reverse()
    else:
        groups = groups.order_by('title')
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
