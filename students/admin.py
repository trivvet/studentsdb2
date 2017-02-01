# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.shortcuts import reverse

from modeltranslation.admin import TranslationAdmin

from .models import Student, Group, Exam, Result, MonthJournal, LogEntry

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

class StudentAdmin(TranslationAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name', 'first_name']
    list_filter = ['student_group']
    list_per_page = 5
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    form = StudentFormAdmin
    actions = ['made_copies']

    #class Media:
        #js = (
            #'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            #'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            #'modeltranslation/js/tabbed_translation_fields.js',
        #)
        #css = {
            #'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        #}

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

    def made_copies(modeladmin, request, queryset):
        for student in queryset.all():
            new_queryset = Student(
                first_name=student.first_name, last_name=student.last_name,
                middle_name=student.middle_name, birthday=student.birthday,
                photo=student.photo, student_group=student.student_group,
                ticket=student.ticket, notes=student.notes)
            new_queryset.save()
    made_copies.short_description = u"Копіювати обраних студентів"

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
admin.site.register(MonthJournal)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(LogEntry)



