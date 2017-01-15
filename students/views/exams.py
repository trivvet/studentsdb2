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

    # take all exams than didn't graded  
    exams = Exam.objects.all().filter(is_completed=False)
    
    # check whether group selected
    current_group = get_current_group(request)
    if current_group:
        exams = exams.filter(exam_group=current_group)
    
    # exams ordering
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('id', 'name', 'date', 'teacher_name', 'exam_group__title'):
        exams = exams.order_by(order_by)
        if reverse == '1':
            exams = exams.reverse()
    else:
        exams = exams.order_by('date')

    # transfer finished exams to the end of list and mark then as completed
    future_exams = []
    finish_exams = []
    for exam in exams:
        if exam.date > datetime.now(timezone.utc):
            future_exams.append(exam)
        else:
            exam.is_completed = True
            finish_exams.append(exam)

    total_exams = future_exams + finish_exams

    # exams paginator
    context = paginate(total_exams, 3, request, {}, var_name='exams')
  
    return render(request, 'students/exams.html', {'context': context})

# Form Class
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

        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False
        
        # set form tag attributes
        if add_form:
            self.helper.action = reverse('exams_add')
        else:
            self.helper.action = reverse_lazy('exams_edit', kwargs['instance'].id)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
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

# Add Form View
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

# Update Form View
class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'students/form_class.html'
    form_class = ExamAddForm
    
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

# Delete Exam Form
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
