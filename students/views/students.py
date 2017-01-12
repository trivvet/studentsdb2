# -*- coding: utf-8 -*-

from datetime import datetime
from PIL import Image

from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.forms import ModelForm, ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.students import Student
from ..models.groups import Group
from ..util import paginate, get_current_group

# Student List

def students_list(request):
  
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        # if check we show students only selected group
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()
    
    # try to order student list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket', 'id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        # default is sorting by last_name of students
        students = students.order_by('last_name')

    # paginator (lay in util.py)
    context = paginate(students, 3, request, {}, var_name='students')
        
    # realisation checkboxes for group action
    message_error = 0
    if request.method == "POST":

        # if press act-button
        if request.POST.get('action_button'):

            # check if we selected at least one student and selected need action
            if request.POST.get('action-group') == 'delete' and request.POST.get('delete-check'):
                students_delete = []
                students_id = []

                for el in request.POST.getlist('delete-check'):
                    try:
                        # try get students from list
                        students_delete.append(Student.objects.get(pk=int(el)))
                        students_id.append(el)
                    except:
                        # otherwise return error message
                        message_error += 1
                        messages.danger(request,
                            u"Будь-ласка, оберіть студентів зі списку")
                if message_error == 0:
                    # if not error messages render confirm page
                    return render(request, 'students/students_group_confirm_delete.html', 
                        {'students': students_delete, 'students_id': students_id})
                        
            # if selected action but didn't select students
            elif request.POST.get('action-group') == 'delete':
                messages.error(request, u"Будь-ласка, оберіть хоча б одного студента")

            # if didn't select action
            else:
                messages.warning(request, u"Будь-ласка, оберіть потрібну дію")

        # if we press delete on confirm page        
        elif request.POST.get('delete_button'):
            for el in request.POST.getlist('students_id'):
                try:
                    student_delete = Student.objects.get(pk=int(el))
                    student_delete.delete()
                except:
                    message_error += 1
                    break
            if message_error == 0:
                messages.success(request, u"Студентів успішно видалено")
            else:
                messages.error(request,
                    u"Видалити обраних студентів неможливо, спробуйте пізніше")
                    
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення обраних студентів скасовано")

    return render(request, 'students/students_list.html', 
        {'context': context})

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

# Form Class
class StudentForm(forms.ModelForm):
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
            'birthday': forms.DateInput(
                attrs={'placeholder': u"напр. 1984-06-17"}),
            'ticket': forms.TextInput(attrs={'placeholder': u"напр. 123"}),
            'notes': forms.Textarea(
                attrs={'placeholder': u"Додаткова інформація",
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False

        # set form tag attributes
        if add_form:
            self.helper.action = reverse('students_add')
        else:
            self.helper.action = reverse_lazy('students_edit', kwargs['instance'].id)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-9'


        # add buttons
        if add_form:
            submit = Submit('add_button', u'Додати')
        else:
            submit = Submit('save_button', u'Зберегти')

        self.helper.layout.append(Layout(
            FormActions(
                submit,
                Submit('cancel_button', u'Скасувати', css_class='btn-link')
            )
        ))

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        
        # validate select of group
        if self.instance:
            group = Group.objects.filter(leader=self.instance)
            if len(group) > 0 and cleaned_data.get('student_group') != group[0]:
                self.add_error('student_group', ValidationError(
                    u"Студент є старостою іншої групи"))
        return cleaned_data

# Add Form View
class StudentAddView(CreateView):
    model = Student
    template_name = 'students/form_class.html'
    form_class = StudentForm
    
    # if post form is valid retern success message
    def get_success_url(self):
        messages.success(self.request,
            u"Студента %s успішно додано" % self.object)
        return reverse('home')

    # render form title    
    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання студента'
        return context

    # if cancel_button is pressed return home page
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

# Edit Form View
class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/form_class.html'
    form_class = StudentForm
    
    # if post form is valid retern success message
    def get_success_url(self):
        messages.success(self.request,
            u"Студента %s успішно збережено" % self.object)
        return reverse('home')

    # render form title
    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування студента'
        return context

    # if cancel_button is pressed return home page
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

# Delete Form View
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete_class.html'

    # when post form is valid return success message
    def get_success_url(self):
        messages.success(self.request,
            u"Студента %s успішно видалено" % self.object)
        return reverse('home')

    # if cancel button is pressed render home page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення студента відмінено")
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentDeleteView, self).post(request, *args, **kwargs)


