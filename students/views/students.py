# -*- coding: utf-8 -*-

from datetime import datetime
from PIL import Image

from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.forms import ModelForm, ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.students import Student
from ..models.groups import Group

# Student List

class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'students/student_class_based_view_template.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        """This method adds extra variables to template"""
        # get original context data from parent class
        context = super(StudentList, self).get_context_data(**kwargs)

        # tell template not to show logo on a page
        context['show_logo'] = False

        # return context mapping
        return context

    def get_queryset(self):
      """Order student by last_name."""
      qs = super(StudentList, self).get_queryset()

      # order by last name
      return qs.order_by('last_name')

def students_list(request):
  
    if request.method == "POST":
        if request.POST.get('action'):
            import pdb; pdb.set_trace()

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

    addition['counter'] = 3* (addition['page'] - 1)
    
    groups = Group.objects.all().order_by('title')
        
    return render(request, 'students/students_list.html', 
        {'students': students, 'groups_all': groups, 'addition': addition})

# Add Form View

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
                messages.success(request, u"Студент %s %s успішно доданий" %
                    (student.last_name, student.first_name))
#                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Додавання студента скасовано")
#            status_message = u"Додавання студента скасовано"
        
    if button != 0:    
        return HttpResponseRedirect(reverse('home'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/students_add.html', 
            {'groups_all': groups, 'addition': addition, 'errors': errors })

# Add Form Class
class StudentAddForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'birthday',
              'photo', 'student_group', 'ticket', 'notes']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': u"Введіть ім’я студента"}),
            'last_name': forms.TextInput(
                attrs={'placeholder': u"Введіть прізвище студента"}),
            'middle_name': forms.TextInput(
                attrs={'placeholder': u"Введіть ім’я по-батькові студента"}),
            'birthday': forms.TextInput(
            attrs={'placeholder': u"напр. 1984-06-17"}),
            'ticket': forms.TextInput(attrs={'placeholder': u"напр. 123"}),
            'notes': forms.Textarea(
                attrs={'placeholder': u"Додаткова інформація",
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse('students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'


        # add buttons
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', u'Додати'),
                Submit('cancel_button', u'Скасувати', css_class='btn-link')
            )
        ))

class StudentAddView(CreateView):
    model = Student
    template_name = 'students/form_class.html'
    form_class = StudentAddForm
    
    def get_success_url(self):
        messages.success(self.request,
            u"Студента %s успішно додано" % self.object)
        return reverse('home')
        
    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання студента'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання студента відмінено")
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)
        
# Edit Form View

def students_edit(request, sid):
    groups = Group.objects.all().order_by('title')
    addition = {}
    button = 0
    data = Student.objects.get(pk=sid)
    data.birthday = data.birthday.isoformat()
    
    # errors collections
    errors = {}

    # was for posted?
    if request.method == "POST":

        # Check which button is pressed
        if request.POST.get('add_button') is not None:
        # Press Add Button

            # data for student object
            data.middle_name = request.POST.get('middle_name', '').strip()
            data.notes = request.POST.get('notes')
            
            # Validation
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data.first_name = first_name
                
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data.last_name = last_name
             
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try: 
                    data.birthday = datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1980-01-01)"
                
            photo = request.FILES.get('photo')
            if photo:
                try:
                    Image.open(photo)
                    if photo.size < 1048576:
                        data.photo = photo
                    else:
                        errors['photo'] = u"Завантажте файл не більше 1Мб"
                except:
                    errors['photo'] = u"Завантажте файл зображення"

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білету є обов'язковим"
            else:
                try:
                    int(ticket)
                    if Student.objects.filter(ticket=int(ticket)).count() == 0 or Student.objects.get(pk=sid).ticket == ticket: 
                        data.ticket = int(ticket)
                    else:
                        errors['ticket'] = u"Номер білету повинен бути унікальним"
                except:
                    errors['ticket'] = u"Номер білету повинен складатись тільки з цифр"

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                try:
                    data.student_group = Group.objects.get(pk=student_group)
                except:
                    errors['student_group'] = u"Виберіть групу зі списку"

            # if not errors save save data to database
            if not errors:
                data.save()
                button += 1
                messages.success(request, u"Інформацію про студента %s %s успішно змінено" %
                    (data.last_name, data.first_name))
#                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)
            else:
                addition['student'] = {'id': data.id}

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Редагування студента скасовано")
#            status_message = u"Додавання студента скасовано"
        
    else:
        try:
            addition['student'] = data
        except:
            messages.error(request, u"Оберіть існуючого студента для редагування")
            button = 1
    if button != 0:    
        return HttpResponseRedirect(reverse('home'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/students_edit.html', 
            {'groups_all': groups, 'addition': addition, 'errors': errors })

# Edit Form Class

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'birthday',
              'photo', 'student_group', 'ticket', 'notes']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': u"Введіть ім’я студента"}),
            'last_name': forms.TextInput(
                attrs={'placeholder': u"Введіть прізвище студента"}),
            'middle_name': forms.TextInput(
                attrs={'placeholder': u"Введіть ім’я по-батькові студента"}),
            'birthday': forms.TextInput(
            attrs={'placeholder': u"напр. 1984-06-17"}),
            'ticket': forms.TextInput(attrs={'placeholder': u"напр. 123"}),
            'notes': forms.Textarea(
                attrs={'placeholder': u"Додаткова інформація",
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse_lazy('students_edit', kwargs['instance'].id)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'


        # add buttons
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', u'Зберегти'),
                Submit('cancel_button', u'Скасувати', css_class='btn-link')
            )
        ))

    def clean(self):
        cleaned_data = super(StudentUpdateForm, self).clean()

        group = Group.objects.filter(leader=self.instance)
        if len(group) > 0 and cleaned_data.get('student_group') != group[0]:
            self.add_error('student_group', ValidationError(
                u"Студент є старостою іншої групи"))
        return cleaned_data
    

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/form_class.html'
    form_class = StudentUpdateForm
    
    def get_success_url(self):
        messages.success(self.request,
            u"Студента %s успішно збережено" % self.object)
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування студента'
        return context
        
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування студента відмінено")
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)
        
# Delete Form View

def students_delete(request, sid):
    groups = Group.objects.all().order_by('title')
    addition = {}
    button = 0

    try:
        data = Student.objects.get(pk=sid)
    except:
        messages.error(request, u"Оберіть існуючого студента для видалення")
        button = 1
    else:
        # was for posted?
        if request.method == "POST":

            # Check which button is pressed
            if request.POST.get('delete_button') is not None:
                # Press Delete Button

                messages.success(request, u"Інформацію про студента %s %s видалено" %
                    (data.last_name, data.first_name))
                data.delete()
                button += 1
#               status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)

            elif request.POST.get('cancel_button') is not None:
            # Press Cancel Button
                button += 1
                messages.warning(request, u"Видалення студента скасовано")
#                status_message = u"Додавання студента скасовано"
        
        else:
            try:
                addition['student'] = data
            except:
                messages.error(request, u"Оберіть існуючого студента для видалення")
                button = 1
    if button != 0:    
        return HttpResponseRedirect(reverse('home'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/students_confirm_delete.html', 
            {'groups_all': groups, 'addition': addition})

# Delete Form Class
  
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete_class.html'

    def get_success_url(self):
        messages.success(self.request,
            u"Студента %s успішно видалено" % self.object)
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення студента відмінено")
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentDeleteView, self).post(request, *args, **kwargs)


