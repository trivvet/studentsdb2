from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l

from registration.forms import RegistrationForm as BaseRegistrationForm
from registration.forms import UserModel, UsernameField
from registration.backends.default.views import RegistrationView as BaseRegistrationView

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

# Registration Form View
class RegistrationView(BaseRegistrationView):
    model = User
    template_name = 'students/form_class.html'
    form_class = RegistrationForm
    success_url = 'users:registration_complete'
    
    # if post form is valid retern success message
#    def get_success_url(self, user=None):
#        messages.success(self.request,
#            _(u"User %s registrated successfully") % user.username)
#        return reverse('users:registration_complete')

    # render form title    
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['title'] = _(u'Register Form')
        return context

    # if cancel_button is pressed return home page
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Registration new user canceled"))
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(RegistrationView, self).post(request, *args, **kwargs)

