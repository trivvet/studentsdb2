# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from .students import Student, Group

# Groups List
def groups_list(request):
    groups = Group.objects.all()
    groups_all = groups.order_by('title')

    # groups ordering
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('title', 'leader__last_name', 'id'):
        groups = groups.order_by(order_by)
        if reverse == '1':
            groups = groups.reverse()
    else:
        groups = groups.order_by('title')

    # groups paginator
    if groups.count() > 0:
        number = 3
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        groups_count = groups.count()
        if groups_count > number:
            addition = {'has_other_pages': True}
            num_pages = groups_count / number
            page_range = []
            if groups_count % number > 0:
                num_pages += 1
            for i in range(1, num_pages+1):
                page_range.append(i)
            addition['page_range'] = page_range

        if page > 0 and page < num_pages:
            groups = groups[number*(page-1):number*page]
            addition['page'] = page
        else:
            groups = groups[number*(num_pages-1):groups_count]
            addition['page'] = num_pages
    else:
        addition = {}
    
    return render(request, 'students/groups.html', {'groups': groups,
        'groups_all': groups_all, 'addition': addition})
        
# Add Form
  
def groups_add(request):
    return HttpResponse('<h1>Groups Add Form</h1>')

# Edit Form
  
def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

# Delete Page
  
def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
