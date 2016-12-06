# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

from ..models.students import Student
from ..models.groups import Group
from ..models.exams import Exam

def exams_list(request):
    addition = {}
    groups = Group.objects.all().order_by('title')
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
        'groups_all': groups, 'addition': addition})

# Add Form

def exams_add(request):
    groups_all = Group.objects.all().order_by('title')
    addition = {}
    button = 0
    
    # errors collections
    errors = {}

    # was for posted?
    if request.method == "POST":

        # Check which button is pressed
        if request.POST.get('add_button') is not None:
        # Press Add Button

            data = {
                'notes': request.POST.get('notes')
            }
            
            # Validation
            name = request.POST.get('name', '').strip()
            if not name:
                errors['name'] = u"Назва предмету є обов'язковою"
            else:
                data['name'] = name

            date = request.POST.get('date', '').strip()
            if not date:
                errors['date'] = u"Дата та час проведення іспиту є обов’язковою"
            else:
                try: 
                    data['date'] = datetime.strptime(date, '%Y-%m-%d %H:%M')
                except Exception:
                    errors['date'] = u"Введіть коректний формат дати та часу (напр. 2016-12-12 10:00)"

            teacher_name = request.POST.get('teacher_name', '').strip()
            if not teacher_name:
                errors['teacher_name'] = u"Прізвище вчителя є обов’язковим"
            else:
                data['teacher_name'] = teacher_name

            exam_group = request.POST.get('exam_group', '').strip()
            if not exam_group:
                errors['exam_group'] = u"Оберіть групу для якої буде проводитись іспит"
            else:
                try:
                    data['exam_group'] = Group.objects.get(pk=exam_group)
                except:
                    errors['exam_group'] = u"Виберіть групу зі списку"

            # if not errors save save data to database
            if not errors:
                exam = Exam(**data)
                exam.save()
                button += 1
                messages.success(request, u"Екзамен %s успішно доданий" % exam.name)

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Додавання іспиту скасовано")
#            status_message = u"Додавання студента скасовано"
        
    if button != 0:    
        return HttpResponseRedirect(reverse('exams'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/exams_add.html', 
            {'groups_all': groups_all, 'addition': addition, 'errors': errors })

# Edit Form
  
def exams_edit(request, eid):
    groups_all = Group.objects.all().order_by('title')
    addition = {}
    button = 0

    try:
        data = Exam.objects.get(pk=eid)
        data.date = data.date.strftime('%Y-%m-%d %H:%M')
    except:
        messages.error(request, u"Оберіть існуючий іспит для редагування")
        button = 1
    
    # errors collections
    errors = {}

    # was for posted?
    if request.method == "POST":

        # Check which button is pressed
        if request.POST.get('save_button') is not None:
        # Press Save Button

            # data for group object
            data.notes = request.POST.get('notes')
            
            # Validation
            name = request.POST.get('name', '').strip()
            if not name:
                errors['name'] = u"Назва предмету є обов'язковою"
            else:
                data.name = name

            date = request.POST.get('date', '').strip()
            if not date:
                errors['date'] = u"Дата та час проведення іспиту є обов’язковою"
            else:
                try: 
                    data.date = datetime.strptime(date, '%Y-%m-%d %H:%M')
                except Exception:
                    errors['date'] = u"Введіть коректний формат дати та часу (напр. 2016-12-12 10:00)"

            teacher_name = request.POST.get('teacher_name', '').strip()
            if not teacher_name:
                errors['teacher_name'] = u"Прізвище вчителя є обов’язковим"
            else:
                data.teacher_name = teacher_name

            exam_group = request.POST.get('exam_group', '').strip()
            if not exam_group:
                errors['exam_group'] = u"Оберіть групу для якої буде проводитись іспит"
            else:
                try:
                    data.exam_group = Group.objects.get(pk=exam_group)
                except:
                    errors['exam_group'] = u"Виберіть групу зі списку"

            # if not errors save save data to database
            if not errors:
                data.save()
                button += 1
                messages.success(request, u"Інформацію про іспит %s успішно змінено" %
                    data.name)
#                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)
            else:
                addition['exam'] = {'id': data.id}

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Редагування іспиту скасовано")
#            status_message = u"Додавання студента скасовано"
        
    else:
        try:
            addition['exam'] = data
        except:
            messages.error(request, u"Оберіть існуючий іспит для редагування")
            button = 1
    if button != 0:    
        return HttpResponseRedirect(reverse('exams'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/exams_edit.html', 
            {'groups_all': groups_all, 'addition': addition, 'errors': errors })

# Delete Page
  
def exams_delete(request, eid):
    groups_all = Group.objects.all().order_by('title')
    button = 0
    try:
        data = Exam.objects.get(pk=eid)
    except:
        messages.error(request, u"Оберіть існуючий іспит для видалення")
        button = 1

    if request.method == "POST":
        if request.POST.get('delete_button') is not None:
            try: 
                data.delete()
                messages.success(request, u"Іспит %s успішно видалено" % data.name)
                button += 1
            except:
                messages.error(request, u"Оберіть існуючий іспит для видалення")
                button += 1
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, u"Видалення іспиту скасовано")
            button += 1
            
    if button != 0:    
        return HttpResponseRedirect(reverse('exams'))
        
    else:
        return render(request, 'students/exams_confirm_delete.html', 
            {'groups_all': groups_all, 'object': data})
