# -*- coding: utf-8 -*-

from django import forms
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DeleteView, CreateView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.students import Student
from ..models.groups import Group

from ..util import paginate, get_current_group

# Groups List
def groups_list(request):
    current_group = get_current_group(request)
    if current_group:
        # if group is selected return only than group
        groups = Group.objects.filter(pk=current_group.id)
    else:
        # otherwise show all students
        groups = Group.objects.all()
  
    # groups ordering
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('title', 'leader__last_name', 'id'):
        groups = groups.order_by(order_by)
        if reverse == '1':
            groups = groups.reverse()
    else:
        groups = groups.order_by('title')

    # groups paginator
    context = paginate(groups, 3, request, {}, var_name='groups')

    return render(request, 'students/groups.html', {'context': context})
        
# Add Form  
def groups_add(request):
    addition = {}
    addition['students_all'] = Student.objects.all().order_by('last_name')
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
                'notes': request.POST.get('notes')
            }
            
            # Validation
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва групи є обов'язковою"
            else:
                data['title'] = title

            # if not errors save save data to database
            if not errors:
                group = Group(**data)
                group.save()
                button += 1
                messages.success(request, u"Група %s успішно додана" % group.title)
#                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Додавання групи скасовано")
#            status_message = u"Додавання студента скасовано"
        
    if button != 0:    
        return HttpResponseRedirect(reverse('groups'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/groups_add.html', 
            {'addition': addition, 'errors': errors })

# Add Form Class
class GroupAddForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'notes']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': u"Введіть назву групи"}),
            'notes': forms.Textarea(
                attrs={'placeholder': u"Додаткова інформація про групу",
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(GroupAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse('groups_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
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

# Add Form View
class GroupAddView(CreateView):
    model = Group
    template_name = 'students/form_class.html'
    form_class = GroupAddForm
    
    # if post form is valid return success message
    def get_success_url(self):
        messages.success(self.request,
            u"Група %s успішно додана" % self.object.title)
        return reverse('groups')

    # render form title    
    def get_context_data(self, **kwargs):
        context = super(GroupAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання групи'
        return context

    # if cancel button is pressed render groups page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання групи відмінено")
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)

# Edit Form  
def groups_edit(request, gid):
    addition = {}
    button = 0
    addition['students_all'] = Student.objects.all().order_by('last_name')

    try:
        data = Group.objects.get(pk=gid)
    except:
        messages.error(request, u"Оберіть існуючу групу для редагування")
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
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва групи є обов'язковою"
            else:
                data.title = title

            leader = request.POST.get('leader', '').strip()
            if leader:
                try:
                    data.leader = Student.objects.get(pk=leader)
                except:
                    errors['leader'] = u"Виберіть студента зі списку"

            # if not errors save save data to database
            if not errors:
                data.save()
                button += 1
                messages.success(request, u"Інформацію про групу %s успішно змінено" %
                    data.title)
#                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)
            else:
                addition['group'] = {'id': data.id}

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Редагування групи скасовано")
#            status_message = u"Додавання студента скасовано"
        
    else:
        try:
            addition['group'] = data
        except:
            messages.error(request, u"Оберіть існуючу групу для редагування")
            button = 1
    if button != 0:    
        return HttpResponseRedirect(reverse('groups'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/groups_edit.html', 
            {'addition': addition, 'errors': errors })

# Edit Form Class
class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': u"Введіть назву групи"}),
            'notes': forms.Textarea(
                attrs={'placeholder': u"Додаткова інформація про групу",
                       'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['leader'].queryset = Student.objects.filter(
            student_group=kwargs['instance'].id)

        # set form tag attributes
        self.helper.action = reverse_lazy('groups_edit', kwargs['instance'].id)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-9'

        # add buttons
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', u'Зберегти'),
                Submit('cancel_button', u'Скасувати', css_class='btn-link')
            )
        ))

# Edit Form View
class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/form_class.html'
    form_class = GroupUpdateForm
    
    def get_success_url(self):
        messages.success(self.request,
            u"Група %s успішно збережена" % self.object.title)
        return reverse('groups')

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування групи'
        return context
        
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування групи відмінено")
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

# Delete Form
def groups_delete(request, gid):
    button = 0

    try:
        data = Group.objects.get(pk=gid)
    except:
        messages.error(request, u"Оберіть існуючу групу для видалення")
        button = 1

    if request.method == "POST":
        if request.POST.get('delete_button') is not None:
            students_of_group = Student.objects.filter(student_group=data.id)
            if students_of_group:
                messages.error(request, u"Видалення неможливе - в групі %s є студенти" % data.title)
                button += 1
            else:
                try: 
                    data.delete()
                    messages.success(request, u"Групу %s успішно видалено" % data.title)
                    button += 1
                except:
                    messages.error(request, u"Оберіть існуючу групу для видалення")
                    button += 1
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, u"Видалення групи скасовано")
            button += 1
            
    if button != 0:    
        return HttpResponseRedirect(reverse('groups'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/groups_confirm_delete.html', 
            {'object': data})

# Delete Form View
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request,
            u"Групу %s успішно видалено" % self.object.title)
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення групи відмінено")
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupDeleteView, self).post(request, *args, **kwargs)
