from datetime import datetime, date

from django import forms
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.logs import LogEntry

from ..util import paginate, paginate_hand, get_current_group

# View for Journal

class LogsView(PermissionRequiredMixin, TemplateView):
    template_name = 'students/logs_list.html'
    permission_required = 'auth.add_user'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(LogsView, self).get_context_data(**kwargs)

        order_by = self.request.GET.get('order_by', '')
        if order_by in ('signal', 'status', 'log_datetime'):
            logs = LogEntry.objects.all().order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                logs = logs.reverse()
        else:
            logs = LogEntry.objects.all().order_by('log_datetime').reverse()
        context = paginate(logs, 10, self.request, {}, var_name='logs')

        # check if we need to display some specific month
        
        return context

class LogUpdateForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = ['signal', 'status', 'log_datetime', 'info']
        widgets = {
            'signal': forms.TextInput(
                attrs={'placeholder': _l(u"Please enter subject name")}),
            'status': forms.Select(
                choices=(("INFO", "INFO"), ("DEBUG", "DEBUG"), ("WARNING", "WARNING"), ("ERROR", "ERROR"), ("CRITICAL", "CRITICAL"))),
            'teacher_name': forms.DateTimeInput(
                attrs={'placeholder': _l(u"Please enter event time")}),
            'info': forms.Textarea(
                attrs={'placeholder': _l(u"Detailed information about event"),
                       'rows': '10'}),
        }

    def __init__(self, *args, **kwargs):
        super(LogUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse_lazy('logs_edit', kwargs['instance'].id)
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
                Submit('add_button', _(u'Save')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))

class LogUpdateView(PermissionRequiredMixin, UpdateView):
    model = LogEntry
    template_name = 'students/form_class.html'
    form_class = LogUpdateForm
    permission_required = 'auth.delete_user'
    
    def get_success_url(self):
        messages.success(self.request,
            _(u"Event %s saved successfully") % self.object.signal)
        return reverse('logs')

    def get_context_data(self, **kwargs):
        context = super(LogUpdateView, self).get_context_data(**kwargs)
        context['title'] = _(u'Editing event')
        return context
        
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Editing event canceled"))
            return HttpResponseRedirect(reverse('logs'))
        else:
            return super(LogUpdateView, self).post(request, *args, **kwargs)

class LogDeleteView(PermissionRequiredMixin, DeleteView):
    model = LogEntry
    template_name = 'students/logs_confirm_delete.html'
    permission_required = 'auth.delete_user'

    def get_success_url(self):
        messages.success(self.request,
            _(u"Event %s deleted successfully") % self.object.signal)
        return reverse('logs')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Deleting event canceled"))
            return HttpResponseRedirect(reverse('logs'))
        else:
            return super(LogDeleteView, self).post(request, *args, **kwargs)

@permission_required('auth.add_user')
def log_info(request, lid):
    context = {}
    context['log'] = LogEntry.objects.get(pk=int(lid))
    return render(request, 'students/log_info.html', {'context': context})
