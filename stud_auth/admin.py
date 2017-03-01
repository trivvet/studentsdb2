# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import admin as auth_admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import StProfile

class StProfileInline(admin.StackedInline):
    model = StProfile
    verbose_name_plural = _(u'Additional user data')
    fk_name = 'user'

class UserAdmin(auth_admin.ModelAdmin):
    inlines = [
        StProfileInline,
    ]

# replace existing User admin form
admin.site.unregister(User)
admin.site.register(User, UserAdmin) 
