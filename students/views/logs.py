# -*- coding: utf-8 -*-

from datetime import datetime, date

from django import forms
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, DeleteView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.logs import LogEntry

from ..util import paginate, paginate_hand, get_current_group

# View for Journal

class LogsView(TemplateView):
    template_name = 'students/logs_list.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(LogsView, self).get_context_data(**kwargs)

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
                attrs={'placeholder': u"Введіть назву предмету"}),
            'status': forms.Select(
                choices=(("INFO", "INFO"), ("DEBUG", "DEBUG"), ("WARNING", "WARNING"), ("ERROR", "ERROR"), ("CRITICAL", "CRITICAL"))),
            'teacher_name': forms.DateTimeInput(
                attrs={'placeholder': u"Введіть час події"}),
            'info': forms.Textarea(
                attrs={'placeholder': u"Детальна інформація про подію",
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
                Submit('add_button', u'Зберегти'),
                Submit('cancel_button', u'Скасувати', css_class='btn-link')
            )
        ))

class LogUpdateView(UpdateView):
    model = LogEntry
    template_name = 'students/form_class.html'
    form_class = LogUpdateForm
    
    def get_success_url(self):
        messages.success(self.request,
            u"Подія %s успішно збережена" % self.object.signal)
        return reverse('logs')

    def get_context_data(self, **kwargs):
        context = super(LogUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування події'
        return context
        
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування події відмінено")
            return HttpResponseRedirect(reverse('logs'))
        else:
            return super(LogUpdateView, self).post(request, *args, **kwargs)

class LogDeleteView(DeleteView):
    model = LogEntry
    template_name = 'students/logs_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request,
            u"Подія %s успішно видалена" % self.object.signal)
        return reverse('logs')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення події відмінено")
            return HttpResponseRedirect(reverse('logs'))
        else:
            return super(LogDeleteView, self).post(request, *args, **kwargs)

def log_info(request, lid):
    context = {}
    context['log'] = LogEntry.objects.get(pk=int(lid))
    return render(request, 'students/log_info.html', {'context': context})
