# -*- coding: utf-8 -*-

import logging

from django import forms, dispatch
from django.shortcuts import render, reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from studentsdb.settings import ADMIN_EMAIL
from ..signals import send_mail_done

class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        # set form tag attributes
        self.helper.action = reverse('contact_admin')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal contact-form'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'


        # add buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))

    from_email = forms.EmailField(
        label=u"Ваша Емейл Адреса")

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2560,
        widget=forms.Textarea)


class ContactView(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm

    def get_success_url(self):
        if self.message:
            messages.success(self.request, u"Лист успішно відправлений")
        else:
            messages.error(self.request, u"Під час відправки листа виникла непередбачувана помилка. Спробуйте скористатись даною формою пізніше")
        return reverse('home')

    def form_valid(self, form):

        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']

        try:
            send_mail(subject, message, from_email, [ADMIN_EMAIL])
            send_mail_done.send(sender=self.__class__, subject=subject, from_email=from_email)
        except Exception:
            message = u'Під час відправки листа виникла непередбачувана помилка. Спробуйте скористатись даною формою пізніше'
            logger = logging.getLogger(__name__)
            logger.exception(message)
            self.message = False
        else:
            self.message = True

        return super(ContactView, self).form_valid(form)



               

           
