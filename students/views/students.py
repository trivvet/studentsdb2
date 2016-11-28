# -*- coding: utf-8 -*-

from datetime import datetime
from PIL import Image

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.forms import ModelForm

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

    # was for posted?
    if request.method == "POST":

        # Check which button is pressed
        if request.POST.get('add_button') is not None:
        # Press Add Button

            # data for student object
            data = {
                'middle_name': request.POST.get('middle_name'),
                'notes': request.POST.get('notes')
            }
            
            # Validation
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
                
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
                
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try: 
                    data['birthday'] = datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1980-01-01)"
                
            photo = request.FILES.get('photo')
            if photo:
                try:
                    Image.open(photo)
                    if photo.size < 1048576:
                        data['photo'] = photo
                    else:
                        errors['photo'] = u"Завантажте файл не більше 1Мб"
                except:
                    errors['photo'] = u"Завантажте файл зображення"

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білету є обов'язковим"
            else:
                try:
                    if not Student.objects.filter(ticket=int(ticket)):
                        data['ticket'] = int(ticket)
                    else:
                        errors['ticket'] = u"Номер білету повинен бути унікальним"
                except:
                    errors['ticket'] = u"Номер білету повинен складатись тільки з цифр"

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                try:
                    data['student_group'] = Group.objects.get(pk=student_group)
                except:
                    errors['student_group'] = u"Виберіть групу зі списку"

            # if not errors save save data to database
            if not errors:
                student = Student(**data)
                student.save()
                button += 1
                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
                                student.first_name)

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            status_message = u"Додавання студента скасовано"
        
    if button != 0:    
        return HttpResponseRedirect(u"%s?status_message=%s" %
               (reverse('home'), status_message))
    else:
        return render(request, 'students/students_add.html', 
            {'groups_all': groups, 'addition': addition, 'errors': errors })

# Edit Form
        
class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    fields = ['first_name', 'last_name', 'middle_name', 'birthday',
              'photo', 'student_group', 'ticket', 'notes']
#    form_class = StudentUpdateForm
    
    @property
    def success_url(self):
        return u"%s?status_message=Студента успішно збережено!" % reverse('home')
        
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                   u"%s?status_message=Редагування студента відмінено!" % 
                   reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)
        
      

# def students_edit(request, sid):
#    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

# Delete Page
  
def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
