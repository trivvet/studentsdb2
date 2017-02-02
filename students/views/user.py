import logging
import pytz

from django import forms, dispatch
from django.shortcuts import render, reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import translation, timezone
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.utils.deprecation import MiddlewareMixin
from django.forms import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.users import MainUser

class UserRegisterForm(forms.ModelForm):

    class Meta:
        choices = pytz.common_timezones
        choices_list = [('', _l(u'Select your time zone'))]
        for value in choices:
            choices_list.append((value, value))
        model = MainUser
        fields = ['username', 'last_name', 'first_name', 'email', 'language', 'time_zone', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': _l(u"Please, enter your username")}),
            'last_name': forms.TextInput(
                attrs={'placeholder': _l(u"Please, enter your last name")}),
            'first_name': forms.TextInput(
                attrs={'placeholder': _l(u"Please, enter your first name")}),
            'email': forms.EmailInput(
                attrs={'placeholder': _l(u"Please, enter your email")}),
            'language': forms.Select(
                choices=(("en", _l(u"English")), ("uk", _l(u"Ukranian")), ("ru", _l("Russian")))),
            'time_zone': forms.Select(
                choices=choices_list),
            'password': forms.PasswordInput(
                attrs={'placeholder': _l(u"Please, enter your password")},
                render_value=False),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        
        # set form tag attributes
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
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', _(u'Register')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))


class UserRegisterView(FormView):
    template_name = 'students/form_class_anonymous.html'
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
        language = form.cleaned_data['language']
        time_zone = form.cleaned_data['time_zone']

        try:
            MainUser.objects.create_user(username=username, email=email, password=password, last_name=last_name, first_name=first_name, language=language, time_zone=time_zone)
        except Exception:
            self.message = False
        else:
            self.message = True

        return super(UserRegisterView, self).form_valid(form)

class UserAuthForm(forms.ModelForm):

    class Meta:
        model = MainUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserAuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        
        # set form tag attributes
        self.helper.action = reverse('user-auth')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.attrs = {'novalidate': ''}
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
        self.helper.layout.append(Layout(
            FormActions(
                Submit('add_button', _(u'Login')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))

class UserAuthView(FormView):
    template_name = 'students/form_class_anonymous.html'
    form_class = UserAuthForm

    def get_success_url(self):
        if self.message:
            messages.success(self.request, _(u"You authorization successfully"))
        else:
            messages.error(self.request, _(u"When you try to log unexpected error ocured. Please try this service later"))
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(UserAuthView, self).get_context_data(**kwargs)
        context['title'] = _(u'Authorization')
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Authorization canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = MainUser.objects.get(username=username)
            translation.activate(current_user.language)
            timezone.activate(current_user.time_zone)
            request.session[translation.LANGUAGE_SESSION_KEY] = current_user.language
            request.session['django_timezone'] = current_user.time_zone
            messages.success(request, _(u"You're logged in as %s" % username))
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, _(u"User with such username or password doesn't exist"))
            return HttpResponseRedirect(reverse('home'))

def user_logout(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('home'))

def user_preference(request):
    if request.method == 'POST':
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Changing user settings canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            current_user = MainUser.objects.get(username=request.user.username)
            data = 0
            first_name=request.POST.get('first_name', '').strip()
            if first_name:
                current_user.first_name = first_name
                data += 1

            last_name=request.POST.get('last_name', '').strip()
            if first_name:
                current_user.last_name = last_name
                data += 1

            email=request.POST.get('email', '').strip()
            if email:
                current_user.email = email
                data += 1

            language=request.POST.get('lang')
            if current_user.language != language:
                current_user.language = language
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = language
                data += 1

            time_zone=request.POST.get('time_zone')
            current_user.time_zone = time_zone
            timezone.activate(time_zone)
            request.session['django_timezone'] = time_zone

            if data > 0:
                current_user.save()
                
            if request.POST.get('newpassword'):
                password = request.POST.get('newpassword')
                if request.POST.get('newpassword2') and password == request.POST.get('newpassword2'):
                    current_user.set_password(password)
                    current_user.save()
                    user = authenticate(username=current_user, password=password)
                    login(request, user)
                    messages.success(request, _(u"User settings changed successfully"))
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request, _(u"Both passwords must be the same"))
                    return render(request, 'students/user_preference.html', {})
            else:
                messages.success(request, _(u"User settings changed successfully"))
                return HttpResponseRedirect(reverse('home'))
    else:
        current_user = MainUser.objects.get(username=request.user.username)
        return render(request, 'students/user_preference.html', {'current_user': current_user, 'timezones': pytz.common_timezones})


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

           
