import logging
import pytz

from django import forms, dispatch
from django.shortcuts import render, reverse
from django.contrib import messages
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.tokens import default_token_generator
from django.utils import translation, timezone
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.forms import ValidationError
from django.template import loader

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from studentsdb.settings import EMAIL_HOST_USER
from stud_auth.models import StProfile
from ..util import paginate

class UserAuthForm(forms.ModelForm):

    class Meta:
        model = User
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
            current_user = User.objects.get(username=username)
            translation.activate(current_user.language)
            if current_user.time_zone:
                timezone.activate(current_user.time_zone)
            request.session[translation.LANGUAGE_SESSION_KEY] = current_user.language
            request.session['django_timezone'] = current_user.time_zone
            messages.success(request, _(u"You're logged in as %s" % username))
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, _(u"User with such username or password doesn't exist"))
            return HttpResponseRedirect(reverse('home'))

def user_preference(request):
    if request.method == 'POST':
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Changing user settings canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            current_user = User.objects.get(username=request.user.username)
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

            try:
                stprofile = StProfile.objects.get(user=current_user)
            except:
                stprofile = StProfile.objects.create(user=current_user)
            data2 = 0
            
            language=request.POST.get('lang')
            if stprofile.language != language:
                stprofile.language = language
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = language
                data2 += 1

            time_zone=request.POST.get('time_zone')
            if stprofile.time_zone != time_zone:
                stprofile.time_zone = time_zone
                timezone.activate(time_zone)
                request.session['django_timezone'] = time_zone
                data2 += 1

            if data > 0:
                current_user.save()

            if data2 > 0:
                stprofile.save()
                
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
        current_user = User.objects.get(username=request.user.username)
        return render(request, 'students/user_preference.html', {'current_user': current_user, 'timezones': pytz.common_timezones})


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

def user_time(request):
    try:
        stprofile = StProfile.objects.get(user=request.user)
        timezone.activate(stprofile.time_zone)
        request.session['django_timezone'] = stprofile.time_zone
    except:
        pass
    try:
        translation.activate(stprofile.language)
        request.session[translation.LANGUAGE_SESSION_KEY] = stprofile.language
    except:
        pass
    messages.success(request, _(u"You have successfully logged in"))
    return HttpResponseRedirect(reverse('home'))

def users_list(request):
    users = User.objects.all()

    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'username', 'date_joined'):
        users = users.order_by(order_by)
        if request.GET.get('reverse') == '1':
            users = users.reverse()
    else:
        users = users.order_by('username')

    context = paginate(users, 3, request, {}, var_name='users')
    
    return render(request, 'students/users_list.html', {'context': context})

def users_profile(request, uid):
    try:
        user = User.objects.get(pk=uid)
    except:
        messages.error(_(u'There was an error on the server. Please try again later'))
    context = {}
    context['user_one'] = user

    return render(request, 'students/user_profile.html', {'context': context})

# User Delete Function
@permission_required('auth.delete_user')
def user_delete(request, uid):
    try:
        user = User.objects.get(pk=uid)
    except:
        messages.error(request, _(u'There was an error on the server. Please try again later'))
        return HttpResponseRedirect(reverse('users'))
    if request.method == 'GET':
        return render(request, 'students/users_confirm_delete.html', {'user_one':user})
    elif request.method == 'POST':
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Deleting user canceled"))
        elif request.POST.get('delete_button'):
            user.delete()
            messages.success(request, _(u"User %s deleted successfully" % user.username))
        return HttpResponseRedirect(reverse('users'))
