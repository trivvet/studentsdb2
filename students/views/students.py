# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse

from ..models.students import Student
from ..models.groups import Group

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
    if students.count() > 0:
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
    else:
        addition = {}
    # end handmade paginator
    
    groups = Group.objects.all().order_by('title')
    
    return render(request, 'students/students_list.html', 
        {'students': students, 'groups_all': groups, 'addition': addition})

# Add Form

def students_add(request):
    groups = Group.objects.all().order_by('title')
    addition = {}
    button = 0
    
    # errors collections
    errors = {}
    # Main Logic
    if request.method == "POST":
        # Check which button is pressed
        
        if request.POST.get('add_button') is not None:
        # Press Add Button
            # data for student object
            data = {}
            
            # Validation
            first_name = request.POST.get('first_name').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
                
            last_name = request.POST.get('last_name').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
                
            birthday = request.POST.get('birthday').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try: 
                    datetime.strptime(birthday, '%Y-%m-%d')
                except:
                    errors['birthday'] = u"Введіть коректне значення дати"
                
            # TODO add validation for other fields
            
            if not errors:
                student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=request.POST['middle_name'],
                    birthday=request.POST['birthday'],
                    photo=request.FILES['photo'],
                    ticket=request.POST['ticket'],
                    student_group=Group(pk=request.POST['student_group']),
                    notes=request.POST['notes'])
                student.save()
                button += 1

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
        
    if button != 0:    
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'students/students_add.html', 
            {'groups_all': groups, 'addition': addition, 'errors': errors })

# Edit Form

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

# Delete Page
  
def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
