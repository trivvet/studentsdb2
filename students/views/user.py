import logging

from django import forms, dispatch
from django.shortcuts import render, reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy
from django.forms import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label=_lazy(u"Confirm password"),
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'placeholder':_(u"Please, cofirm your password")}
        )
    )

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': _(u"Please, enter your username")}),
            'last_name': forms.TextInput(
                attrs={'placeholder': _(u"Please, enter your last name")}),
            'first_name': forms.TextInput(
                attrs={'placeholder': _(u"Please, enter your first name")}),
            'email': forms.EmailInput(
                attrs={'placeholder': _(u"Please, enter your email")}),
            'password': forms.PasswordInput(
                attrs={'placeholder': _(u"Please, enter your password")},
                render_value=False),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        try:
            kwargs['instance']
        except:
            kwargs['instance'] = None
            
        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False
        
        # set form tag attributes
#        if add_form:
#            self.helper.action = reverse('user_add')
#       else:
        self.helper.action = reverse('user-register')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
        if add_form:
            submit = Submit('add_button', _(u'Register'))
        else:
            submit = Submit('save_button', _(u'Save Change'))
            
        self.helper.layout.append(Layout(
            FormActions(
                submit,
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        try:
            password = cleaned_data['password']
            password2 = cleaned_data['password2']
        except:
            password = None
            password2 = None
        # validate confirm password
        if password and password2 and password != password2:
            self.add_error('password2', ValidationError(_(u"Both passwords must be the same")))
            
        return cleaned_data


class UserRegisterView(FormView):
    template_name = 'students/form_class.html'
    form_class = UserRegisterForm

    def get_success_url(self):
        if self.message:
            messages.success(self.request, _(u"User %s registered successfully") % self.request.POST.get('username'))
        else:
            messages.error(self.request, _(u"When registration new user unexpected error ocured. Please try this service later"))
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['title'] = _(u'User Regiser')
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Register user canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(UserRegisterView, self).post(request, *args, **kwargs)

    def form_valid(self, form):

        last_name = form.cleaned_data['last_name']
        first_name = form.cleaned_data['first_name']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']


        try:
            User.objects.create_user(username=username, email=email, password=password, last_name=last_name, first_name=first_name)
        except Exception:
            self.message = False
        else:
            self.message = True

        return super(UserRegisterView, self).form_valid(form)



               

           
