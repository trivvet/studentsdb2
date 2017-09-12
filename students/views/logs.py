from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django import forms
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User

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

        prev_date = timezone.now() - relativedelta(months=1)
        logs_delete = LogEntry.objects.exclude(log_datetime__gt=prev_date)
        if logs_delete:
            for log in logs_delete:
                log.delete()

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

    # realisation checkboxes for group action
    def post(self, request, *args, **kwargs):
        message_error = 0
        # if press act-button
        if request.POST.get('action_button'):

            logs_delete = []
            logs_id = []
                
            # check if we selected at least one log and selected need action
            if request.POST.get('action-group') == 'delete' and request.POST.get('delete-check'):

                for el in request.POST.getlist('delete-check'):
                    if el != 'all':
                        try:
                            # try get logs from list
                            logs_delete.append(LogEntry.objects.get(pk=int(el)))
                            logs_id.append(el)
                        except:
                            # otherwise return error message
                            message_error += 1
                            messages.error(request,
                                _(u"Please, select log from list"))

            # if selected action but didn't select students
            elif request.POST.get('action-group') == 'delete':
                message_error += 1
                messages.error(request, _(u"Please, select at least one log"))

            elif request.POST.get('action-group') == 'all_delete':
                logs = LogEntry.objects.all()
                if logs.count() < 10:
                    for log in LogEntry.objects.all():
                        logs_delete.append(log)
                        logs_id.append(log.id)
                else:
                    logs_delete = {
                        'danger':_("You really want to delete all %d logs") % logs.count()}
                    for log in logs:
                        logs_id.append(log.id)

            # if didn't select action
            else:
                message_error += 1
                messages.warning(request, _(u"Please, select the desired action"))

            if message_error == 0:
                # if not error messages render confirm page
                return render(request, 'students/students_group_confirm_delete.html',
                    {'logs': logs_delete, 'logs_id': logs_id})

        # if we press delete on confirm page
        elif request.POST.get('delete_button'):
            for el in request.POST.getlist('logs_id'):
                try:
                    log_delete = LogEntry.objects.get(pk=int(el))
                    log_delete.delete()
                except:
                    message_error += 1
                    break
            if message_error == 0:
                messages.success(request, _(u"Logs successfully removed"))
            else:
                messages.error(request,
                    _(u"Selected logs can't delete, try later"))
            return HttpResponseRedirect(reverse('logs'))

        elif request.POST.get('cancel_button'):
            messages.warning(request, _(u"Delete of selected student canceled"))
            
        return HttpResponseRedirect(reverse('logs'))

class LogUpdateForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = ['signal', 'status', 'log_datetime', 'info']
        widgets = {
            'signal': forms.TextInput(
                attrs={'placeholder': _l(u"Please enter subject name")}),
            'status': forms.Select(
                choices=(("INFO", "INFO"), ("DEBUG", "DEBUG"), ("WARNING", "WARNING"), ("ERROR", "ERROR"), ("CRITICAL", "CRITICAL"))),
            'log_datetime': forms.DateTimeInput(
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
    log_object = LogEntry.objects.get(pk=int(lid))
    if log_object.created_by:
        try:
            context['created_by'] = User.objects.get(pk=log_object.created_by.id).username
        except AttributeError:
            context['created_by'] = _(u'User with id %s, who was deleted') % log_object.created_by.id
    if log_object.modified_by:
        try:
            context['modified_by'] = User.objects.get(pk=log_object.modified_by.id).username
        except AttributeError:
            context['modified_by'] = _(u'User with id %s, who was deleted') % log_object.modified_by.id
    context['time_change'] = log_object.time_change
    context['log'] = LogEntry.objects.get(pk=int(lid))
    return render(request, 'students/log_info.html', {'context': context})
