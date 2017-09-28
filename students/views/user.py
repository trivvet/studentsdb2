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

from stud_auth.models import StProfile
from ..util import paginate

def user_preference(request):

    current_user = User.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Changing user settings canceled"))
            return HttpResponseRedirect(reverse('home'))
            
        else:
            errors = {}
            stprofile = StProfile.objects.get_or_create(user=current_user)[0]
            
            form_first_name=request.POST.get('first_name', '').strip()
            current_user.first_name = form_first_name

            form_last_name=request.POST.get('last_name', '').strip()
            current_user.last_name = form_last_name

            form_email=request.POST.get('email', '').strip()
            users_same_email = User.objects.filter(email=form_email)
            if len(users_same_email) > 0 and current_user.email != form_email:
                current_user.email = form_email
                errors['email'] = _(u"This email address is already in use." +
                    " Please enter a different email address.")
            elif len(form_email) > 0:
                try:
                    validate_email(form_email)
                except ValidationError:
                    errors['email'] = _(u"Enter a valid email address")
                else:
                    current_user.email = form_email

            form_language=request.POST.get('lang')
            if stprofile.language != form_language:
                stprofile.language = form_language
                translation.activate(form_language)
                request.session[translation.LANGUAGE_SESSION_KEY] = form_language

            form_time_zone=request.POST.get('time_zone')
            if stprofile.time_zone != form_time_zone:
                stprofile.time_zone = form_time_zone
                timezone.activate(form_time_zone)
                request.session['django_timezone'] = form_time_zone

            if errors:
                messages.error(request, _(u'Please, correct the following errors'))
                return render(request, 'students/user_preference.html',
                    {'current_user': current_user, 'timezones': pytz.common_timezones, 'errors': errors})

            current_user.save()
            stprofile.save()

            messages.success(request, _(u"User settings changed successfully"))
            return HttpResponseRedirect(reverse('home'))

    else:
        return render(request, 'students/user_preference.html',
            {'current_user': current_user, 'timezones': pytz.common_timezones})


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
    messages.success(request, _(u"You have successfully logged in as %s") % request.user.username)
    try:
        translation.activate(stprofile.language)
        request.session[translation.LANGUAGE_SESSION_KEY] = stprofile.language
    except:
        pass
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
            messages.success(request, _(u"User %s deleted successfully") % user.username)
        return HttpResponseRedirect(reverse('users'))
