from datetime import datetime
from PIL import Image
from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import translation, timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.contrib.auth.mixins import LoginRequiredMixin

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from modeltranslation.forms import TranslationModelForm

from ..models.students import Student
from ..models.groups import Group
from ..models.logs import LogEntry
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

    students_list = []
    for student in students:
        if student.first_name:
            students_list.append(student)

    # paginator (lay in util.py)
    context = paginate(students_list, 3, request, {}, var_name='students')
        
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
                            _(u"Please, select student from list"))
                if message_error == 0:
                    # if not error messages render confirm page
                    return render(request, 'students/students_group_confirm_delete.html', 
                        {'students': students_delete, 'students_id': students_id})
                        
            # if selected action but didn't select students
            elif request.POST.get('action-group') == 'delete':
                messages.error(request, _(u"Please, select at least one student"))

            # if didn't select action
            else:
                messages.warning(request, _(u"Please, select the desired action"))

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
                messages.success(request, _(u"Students successfully removed"))
            else:
                messages.error(request,
                    _(u"Selected students can't delete, try later"))
                    
        elif request.POST.get('cancel_button'):
            messages.warning(request, _(u"Delete of selected student canceled"))

    return render(request, 'students/students_list.html', 
        {'context': context})

# Form Class
class StudentForm(TranslationModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'first_name', 'last_name', 'middle_name', 'birthday',
              'photo', 'student_group', 'ticket', 'notes']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': _l(u"Please, type student's first name")}),
            'last_name': forms.TextInput(
                attrs={'placeholder': _l(u"Please, type student's last name")}),
            'middle_name': forms.TextInput(
                attrs={'placeholder': _l(u"Please, type student's middle name")}),
            'birthday': forms.DateInput(
                attrs={'placeholder': _l(u"e.g. 1984-06-17")}, format=('%Y-%m-%d')),
            'ticket': forms.TextInput(attrs={'placeholder': _l(u"e.g. 123")}),
            'notes': forms.Textarea(
                attrs={'placeholder': _l(u"Aditional information"),
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
#        translation.activate(translation.get_language())
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
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-8'


        # add buttons
        if add_form:
            submit = Submit('add_button', _(u'Add'))
        else:
            submit = Submit('save_button', _(u'Save'))

        self.helper.layout.append(Layout(
            FormActions(
                submit,
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        
        # validate select of group
        if self.instance:
            group = Group.objects.filter(leader=self.instance)
            if len(group) > 0 and cleaned_data.get('student_group') != group[0]:
                self.add_error('student_group', ValidationError(
                    _(u"Student is leader of other group")))

        # validate birthday
        try:
            cleaned_data['birthday']
        except KeyError:
            cleaned_data['birthday'] = False
        if cleaned_data['birthday']:
            birthday = cleaned_data['birthday']
            min_date = datetime.today().date() - relativedelta(years=17)
            if birthday > min_date:
                self.add_error('birthday', ValidationError(_(u"Student's age can't be less then 17 years")))
                
        return cleaned_data

# Add Form View
class StudentAddView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'students/form_class.html'
    form_class = StudentForm
    
    # if post form is valid retern success message
    def get_success_url(self):
        messages.success(self.request,
            _(u"Student %s created successfully") % self.object)
        return reverse('home')

    # render form title    
    def get_context_data(self, **kwargs):
        if self.kwargs['lang']:
            translation.activate(self.kwargs['lang'])
            language = self.kwargs['lang']
        else:
            language = translation.get_language()

        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = _(u'Adding Student')
        context['lang_add'] = language
        return context

    # if cancel_button is pressed return home page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Adding student canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)
        
# Edit Form View
class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'students/form_class.html'
    form_class = StudentForm
    
    # if post form is valid retern success message
    def get_success_url(self):
        messages.success(self.request,
            _(u"Student %s saved successfully!") % self.object)
        return reverse('home')

    # render form title
    def get_context_data(self, **kwargs):
        if self.kwargs['lang']:
            translation.activate(self.kwargs['lang'])
            language = self.kwargs['lang']
        else:
            language = translation.get_language()
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = _(u'Editing student')
        context['lang'] = language
        context['student_id'] = self.kwargs['pk']
        return context

    # if cancel_button is pressed return home page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Editing student canceled!"))
            return HttpResponseRedirect(reverse('home'))
        else:
            translation.activate(self.kwargs['lang'])
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

# Delete Form View
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete_class.html'

    # when post form is valid return success message
    def get_success_url(self):
        messages.success(self.request,
            _(u"Student %s deleted successfully") % self.object)
        return reverse('home')

    # if cancel button is pressed render home page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Deleting student canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentDeleteView, self).post(request, *args, **kwargs)


