# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from ..models.students import Student
from ..models.groups import Group

# View for Journal

def journal_list(request):
    students = Student.objects.all().order_by('id')

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
    days = []
    day_names = [u'Пн', u'Вт', u'Ср', u'Чт', u'Пт', u'Сб', u'Нд']
    for i in range(1, 31):
        days.append(day_names[i%7-1])
#   import pdb;pdb.set_trace()
    return render(request, 'students/journal.html', 
        {'students': students, 'groups_all': groups, 'days': days, 
         'day_names': day_names, 'addition': addition})


# Create your views here.
