from django.contrib import admin
from django.contrib import admin as auth_admin
from django.contrib.auth.models import User

from .models import StProfile

class StProfileInline(admin.StackedInline):
    model = StProfile

class UserAdmin(auth_admin.ModelAdmin):
    inlines = [
        StProfileInline,
    ]

# replace existing User admin form
admin.site.unregister(User)
admin.site.register(User, UserAdmin) 
