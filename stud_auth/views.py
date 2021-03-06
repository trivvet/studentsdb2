from django import forms
from django.core.validators import validate_slug, validate_email
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l

from registration.forms import RegistrationForm as BaseRegistrationForm
from registration.forms import UserModel, UsernameField
from registration.backends.default.views import RegistrationView as BaseRegistrationView

from social_core.pipeline.partial import partial

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit

User = UserModel()

class RegistrationForm(BaseRegistrationForm):
    email = forms.EmailField(
        label=_l(u"E-mail"),
        widget = forms.EmailInput(
            attrs={'placeholder': _l(u"Please, type your email address")}
        )
    )
    password1 = forms.CharField(
        label = _l(u'Password'),
        widget = forms.PasswordInput(
            attrs={'placeholder': _l(u"Please, type your password")},
        )
    )
    password2 = forms.CharField(
        label = _l(u'Confirm password'),
        widget = forms.PasswordInput(
            attrs={'placeholder': _l(u"Please, type password again")},
        )
    )

    class Meta:
        model = User
        fields = (UsernameField(), "email")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.action = reverse('registration_register')
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
                Submit('register_button', _(u'Register')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-link')
            )
        ))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

# Registration Form View
class RegistrationView(BaseRegistrationView):
    model = User
    template_name = 'students/form_class.html'
    form_class = RegistrationForm
    success_url = 'users:registration_complete'

    # render form title
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['title'] = _(u'Register Form')
        context['user_check'] = reverse('user_check')
        return context

    # if cancel_button is pressed return home page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Registration new user canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(RegistrationView, self).post(request, *args, **kwargs)

@partial
def get_user_name(backend, details, response, is_new=False, *args, **kwargs):
    request = backend.strategy.request
    errors = {}
    if is_new==False:
        return {}
    if request.method == 'GET':
        return render(request, 'stud_auth/select_user_name.html', {})
    else:
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Entrance is canceled")
            return HttpResponseRedirect(reverse('home'))
        elif request.POST.get('success_button'):
            final_username = request.POST.get('username')
            if final_username != '':
                if len(User.objects.filter(username=final_username)) != 0:
                    errors['username'] = _(u"Sorry, but the same username already exists")
            else:
                errors['username'] = _(u"Please, enter your username")
            if errors:
                return render(request, 'stud_auth/select_user_name.html', {'errors': errors, 'user_name': final_username})
            else:
                return {'username': final_username}

def check_user_name(request):
    data = request.POST
    found = 'not_found'
    error = ''
    if 'username' in data.values():
        if User.objects.filter(username=data['field_value']):
            found = 'success'
            error = _(u"Sorry, but the same username already exists")
        elif data['field_value'] == '':
            found = 'success'
            error = _(u"Please, enter your username")
        try:
            validate_slug(data['field_value'])
        except ValidationError:
            found = 'success'
            error = _("Enter a valid username consisting of letters, numbers, underscores or hyphens.")
            
    elif 'email' in data.values():
        if User.objects.filter(email=data['field_value']) and data['field_value'] != '':
            found = 'success'
            error = _(u"Sorry, but this email address is already in use")
        elif data['field_value'] == '':
            found = 'success'
            error = _(u"Please, enter your email")
        try:
            validate_email(data['field_value'])
        except ValidationError as message:
            found = 'success'
            error = message[0]

    elif 'password1' in data.values():
        if len(data['field_value']) < 8:
            found = 'success'
            error = _(u"This password is too short. It must contain at least 8 characters.")
        try:
            validate_slug(data['field_value'])
        except ValidationError:
            found = 'success'
            error = _("Enter a valid password consisting of letters, numbers, underscores or hyphens.")
    
        
    return JsonResponse({'status': 'success', 'if_found': found, 'error': error})
