# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import reverse

from .models.students import Student
from .models.groups import Group
from .models.exams import Exam
from .models.results import Result

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name', 'first_name']
    list_filter = ['student_group']
    list_per_page = 5
    search_fields = ['last_name', 'first_name', 'ticket', 'notes']

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_editable = ['leader']
    ordering = ['title']
    list_per_page = 5
    search_fields = ['title']

#    def view_on_site(self, obj):
#        return reverse('groups_edit', kwargs={'pk': obj.id})

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Result)
