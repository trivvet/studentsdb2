from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import admin as user_admin

from .models import StProfile

class StProfileInline(admin.StackedInline):
    model = StProfile

class UserAdmin(user_admin.UserAdmin):
    inlines = (StProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin) 
