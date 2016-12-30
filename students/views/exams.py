# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DeleteView, CreateView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.students import Student
from ..models.groups import Group
from ..models.exams import Exam

from ..util import paginate, get_current_group

def exams_list(request):
    current_group = get_current_group(request)
    if current_group:
        exams = Exam.objects.filter(exam_group=current_group)
    else:
        exams = Exam.objects.all()
    
    # exams ordering
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('id', 'name', 'date', 'teacher_name', 'exam_group__title'):
        exams = exams.order_by(order_by)
        if reverse == '1':
            exams = exams.reverse()
    else:
        exams = exams.order_by('date').reverse()

    future_exams = []
    for exam in exams:
        if exam.date > datetime.now(timezone.utc):
            future_exams.append(exam)

    # groups paginator
    context = paginate(future_exams, 3, request, {}, var_name='exams')
  
    return render(request, 'students/exams.html', {'context': context})

# Add Form

def exams_add(request):
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
            {'addition': addition, 'errors': errors })

# Add Form Class
class ExamAddForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'teacher_name', 'exam_group', 'notes']
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': u"Введіть назву предмету"}),
            'date': forms.DateTimeInput(
                attrs={'placeholder': u"напр. 2016-12-12 10:00"}),
            'teacher_name': forms.TextInput(
                attrs={'placeholder': u"Введіть прізвище та ініціали викладача"}),
            'notes': forms.Textarea(
                attrs={'placeholder': u"Додаткова інформація про іспит",
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExamAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse('exams_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-9'


        # add buttons
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', u'Додати'),
                Submit('cancel_button', u'Скасувати', css_class='btn-link')
            )
        ))

class ExamAddView(CreateView):
    model = Exam
    template_name = 'students/form_class.html'
    form_class = ExamAddForm
    
    def get_success_url(self):
        messages.success(self.request,
            u"Іспит %s успішно доданий" % self.object.name)
        return reverse('exams')
        
    def get_context_data(self, **kwargs):
        context = super(ExamAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання іспиту'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання іспиту відмінено")
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamAddView, self).post(request, *args, **kwargs)

# Edit Form
  
def exams_edit(request, eid):
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
            {'addition': addition, 'errors': errors })

# Edit Form Class

class ExamUpdateForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'teacher_name', 'exam_group', 'notes']
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': u"Введіть назву предмету"}),
            'date': forms.DateTimeInput(
                attrs={'placeholder': u"напр. 2016-12-12 10:00"}),
            'teacher_name': forms.TextInput(
                attrs={'placeholder': u"Введіть прізвище та ініціали викладача"}),
            'notes': forms.Textarea(
                attrs={'placeholder': u"Додаткова інформація про іспит",
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExamUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse_lazy('exams_edit', kwargs['instance'].id)
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

class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'students/form_class.html'
    form_class = ExamUpdateForm
    
    def get_success_url(self):
        messages.success(self.request,
            u"Іспит %s успішно збережено" % self.object.name)
        return reverse('exams')

    def get_context_data(self, **kwargs):
        context = super(ExamUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування іспиту'
        return context
        
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування іспиту відмінено")
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamUpdateView, self).post(request, *args, **kwargs)

# Delete Page
  
def exams_delete(request, eid):
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
            {'object': data})

class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request,
            u"Іспит %s успішно видалено" % self.object.name)
        return reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення іспиту відмінено")
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamDeleteView, self).post(request, *args, **kwargs)
