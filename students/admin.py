# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.shortcuts import reverse

from .models.students import Student
from .models.groups import Group
from .models.exams import Exam
from .models.results import Result

class StudentFormAdmin(ModelForm):
    def clean_student_group(self):
        """Check if student is leader of any group

        If yes, then ensure it's the same as selected group"""
        # get group where current student is a leader
        group = Group.objects.filter(leader=self.instance)
        if len(group) > 0 and self.cleaned_data['student_group'] != group[0]:
            raise ValidationError(u'Студент є старостою іншої групи.',
                code='invalid')
        else:
            return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name', 'first_name']
    list_filter = ['student_group']
    list_per_page = 5
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

class GroupFormAdmin(ModelForm):
    def clean_leader(self):
        """Check if student is leader of any group

        If yes, then ensure it's the same as selected group"""
        # get group where current student is a leader
        students = Student.objects.filter(student_group=self.instance)
        groups = Group.objects.filter(leader=self.cleaned_data['leader'])
        if len(groups) > 0 and groups[0] != self.instance:
            raise ValidationError(u'Студент є старостою іншої групи.',
                code='invalid')
        elif len(students) == 0 or self.cleaned_data['leader'] not in students:
            raise ValidationError(u'Для початку додайте вибраного студента в дану групу', code='invalid')
        else:
            return self.cleaned_data['leader']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_editable = ['leader']
    ordering = ['title']
    list_per_page = 5
    search_fields = ['title']
    form = GroupFormAdmin

#    def view_on_site(self, obj):
#        return reverse('groups_edit', kwargs={'pk': obj.id})

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Result)
