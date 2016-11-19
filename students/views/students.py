# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student, Group

# Student List

def students_list(request):
  
    students = Student.objects.all()
    
    # try to order student list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket', 'id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')

    # paginate students
    """    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver
        # last page of result
        students = paginator.page(paginator.num_pages) """
        
#    import pdb;pdb.set_trace()  
    
    # handmade paginator
    number = 3
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    num_pages = students.count() / number
    if students.count() % number > 0:
        num_pages += 1
    # block for student_list template
    if num_pages > 0:
        page_range = []
        for i in range(1, num_pages+1):
          page_range.append(i)
        addition = {'has_other_pages': True, 'page_range': page_range}
        
    if page > 0 and page < num_pages:
        students = students[number*(page-1):number*page]
        addition['page'] = page
    else:
        students = students[number*(num_pages-1):students.count()]
        addition['page'] = num_pages
    # end handmade paginator
    
    groups = Group.objects.all().order_by('title')
    
    return render(request, 'students/students_list.html', 
        {'students': students, 'groups_all': groups, 'addition': addition})

# Add Form

def students_add(request):
    return HttpResponse('<h1>Students Add Form</h1>')

# Edit Form

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

# Delete Page
  
def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
