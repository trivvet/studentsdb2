# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.views.generic import DeleteView, CreateView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.students import Student
from ..models.groups import Group
from ..models.exams import Exam
from ..models.results import Result

from ..util import paginate, get_current_group

def results_list(request):
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

    exams_result = []

    for exam in exams:
        if exam.date < datetime.now(timezone.utc):
            exams_result.append(exam)

    # groups paginator
    context = paginate(exams_result, 3, request, {}, var_name='results')

    return render(request, 'students/results.html', { 'context': context })
        
def results_add(request):
    return HttpResponse('<h1>Results Add Form</h1>')


# Add Form Class
class ResultAddForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['result_student', 'result_exam', 'score']
        widgets = {
            'score': forms.TextInput(
                attrs={'placeholder': u"Введіть оцінку в балах від 1 до 12"})
        }

    def __init__(self, *args, **kwargs):
        super(ResultAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse('results_add')
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

class ResultAddView(CreateView):
    model = Result
    template_name = 'students/form_class.html'
    form_class = ResultAddForm
    
    def get_success_url(self):
        messages.success(self.request,
            u"Результат %s по %s успішно доданий" % (self.object.result_student, self.object.result_exam))
        return reverse('results')
        
    def get_context_data(self, **kwargs):
        context = super(ResultAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання результату іспиту'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання результату відмінено")
            return HttpResponseRedirect(reverse('results'))
        else:
            return super(ResultAddView, self).post(request, *args, **kwargs)

# Edit Form
  
def results_edit(request, rid):
    return HttpResponse('<h1>Edit Result %s</h1>' % rid)

# Delete Page
  
def results_delete(request, rid):
    return HttpResponse('<h1>Delete Result %s</h1>' % rid)

def exam_results(request, rid):
    return HttpResponse('<h1>Results for %s</h1>' % rid)
