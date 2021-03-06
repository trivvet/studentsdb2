from django import forms
from django.urls import reverse_lazy
from django.utils import translation
from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ValidationError
from django.views.generic import DeleteView, CreateView, UpdateView
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from modeltranslation.forms import TranslationModelForm

from ..models.students import Student
from ..models.groups import Group
from ..models.exams import Exam
from ..models.results import Result

from ..util import paginate, get_current_group

# Groups List
@login_required
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

# Add Form Class
class GroupAddForm(TranslationModelForm):
    class Meta:
        model = Group
        fields = ['title', 'notes']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': _l(u"Type group's title")}),
            'notes': forms.Textarea(
                attrs={'placeholder': _l(u"Additional information about group"),
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
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', _(u'Add')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))

    def clean(self):
        cleaned_data = super(GroupAddForm, self).clean()

        # validate name of group
        groups = Group.objects.filter(title=cleaned_data.get('title'))
        if len(groups) > 0:
            self.add_error('title', ValidationError(
                _(u"Group with the same title already exists")))
        else:
            return cleaned_data

    def save(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields', {})
        fields = extra_fields
        fields.update({k: self.cleaned_data[k] for k in self._meta.fields})
        self.instance = self._meta.model.objects.populate(True).create(
            **fields
        )
        return super(GroupAddForm, self).save(*args, **kwargs)

# Add Form View
class GroupAddView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'students/form_class.html'
    form_class = GroupAddForm

    # if post form is valid return success message
    def get_success_url(self):
        messages.success(self.request,
            _(u"Group %s added successfully") % self.object.title)
        return reverse('groups')

    # render form title
    def get_context_data(self, **kwargs):
        if self.kwargs['lang']:
            translation.activate(self.kwargs['lang'])
            language = self.kwargs['lang']
        else:
            language = translation.get_language()
        context = super(GroupAddView, self).get_context_data(**kwargs)
        context['title'] = _(u'Adding Group')
        context['lang'] = language
        context['action'] = 'groups_add'
        return context

    # if cancel button is pressed render groups page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Adding group canceled"))
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)

# Edit Form Class
class GroupUpdateForm(TranslationModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': _l(u"Type group's title")}),
            'notes': forms.Textarea(
                attrs={'placeholder': _l(u"Addiotional information about group"),
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
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', _(u'Save')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))

# Edit Form View
class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'students/form_class.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        messages.success(self.request,
            _(u"Group %s saved successfully") % self.object.title)
        return reverse('groups')

    def get_context_data(self, **kwargs):
        if self.kwargs['lang']:
            translation.activate(self.kwargs['lang'])
            language = self.kwargs['lang']
        else:
            language = translation.get_language()
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['title'] = _(u'Editing Group')
        context['lang'] = language
        context['action'] = 'groups_edit'
        context['item_id'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Editing group canceled"))
            return HttpResponseRedirect(reverse('groups'))
        else:
            translation.activate(self.kwargs['lang'])
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

# Delete Form View
class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request,
            _(u"Group %s deleted successfully") % self.object.title)
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Deleting group calceled"))
            return HttpResponseRedirect(reverse('groups'))
        else:
            group = Group.objects.get(pk=kwargs['pk'])
            if Student.objects.filter(student_group=group):
                messages.error(request, _(u"Deletion is impossible. There are students in the group"))
                return HttpResponseRedirect(reverse('groups'))
            else:
                exams = Exam.objects.filter(exam_group=group)
                if exams:
                    for exam in exams:
                        if Result.objects.filter(result_exam=exam):
                            messages.error(request, _(u"Deletion is impossible. There are available results for this group"))
                            return HttpResponseRedirect(reverse('groups'))
                return super(GroupDeleteView, self).post(request, *args, **kwargs)
