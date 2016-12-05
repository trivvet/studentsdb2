# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DeleteView

from ..models.students import Student
from ..models.groups import Group

# Groups List
def groups_list(request):
    groups = Group.objects.all()
    groups_all = groups.order_by('title')

    # groups ordering
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('title', 'leader__last_name', 'id'):
        groups = groups.order_by(order_by)
        if reverse == '1':
            groups = groups.reverse()
    else:
        groups = groups.order_by('title')

    # groups paginator
    if groups.count() > 0:
        number = 3
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        groups_count = groups.count()
        if groups_count > number:
            addition = {'has_other_pages': True}
            num_pages = groups_count / number
            page_range = []
            if groups_count % number > 0:
                num_pages += 1
            for i in range(1, num_pages+1):
                page_range.append(i)
            addition['page_range'] = page_range

        if page > 0 and page < num_pages:
            groups = groups[number*(page-1):number*page]
            addition['page'] = page
        else:
            groups = groups[number*(num_pages-1):groups_count]
            addition['page'] = num_pages
    else:
        addition = {}
    
    return render(request, 'students/groups.html', {'groups': groups,
        'groups_all': groups_all, 'addition': addition})
        
# Add Form
  
def groups_add(request):
    groups_all = Group.objects.all().order_by('title')
    addition = {}
    addition['students_all'] = Student.objects.all().order_by('last_name')
    button = 0
    
    # errors collections
    errors = {}

    # was for posted?
    if request.method == "POST":

        # Check which button is pressed
        if request.POST.get('add_button') is not None:
        # Press Add Button

            # data for student object
            data = {
                'notes': request.POST.get('notes')
            }
            
            # Validation
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва групи є обов'язковою"
            else:
                data['title'] = title

            # if not errors save save data to database
            if not errors:
                group = Group(**data)
                group.save()
                button += 1
                messages.success(request, u"Група %s успішно додана" % group.title)
#                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Додавання групи скасовано")
#            status_message = u"Додавання студента скасовано"
        
    if button != 0:    
        return HttpResponseRedirect(reverse('groups'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/groups_add.html', 
            {'groups_all': groups_all, 'addition': addition, 'errors': errors })

# Edit Form
  
def groups_edit(request, gid):
    groups_all = Group.objects.all().order_by('title')
    addition = {}
    button = 0
    addition['students_all'] = Student.objects.all().order_by('last_name')

    try:
        data = Group.objects.get(pk=gid)
    except:
        messages.error(request, u"Оберіть існуючу групу для редагування")
        button = 1
    
    # errors collections
    errors = {}

    # was for posted?
    if request.method == "POST":

        # Check which button is pressed
        if request.POST.get('save_button') is not None:
        # Press Save Button

            # data for group object
            data.notes = request.POST.get('notes')
            
            # Validation
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва групи є обов'язковою"
            else:
                data.title = title

            leader = request.POST.get('leader', '').strip()
            if leader:
                try:
                    data.leader = Student.objects.get(pk=leader)
                except:
                    errors['leader'] = u"Виберіть студента зі списку"

            # if not errors save save data to database
            if not errors:
                data.save()
                button += 1
                messages.success(request, u"Інформацію про групу %s успішно змінено" %
                    data.title)
#                status_message = u"Студент %s %s успішно доданий" % (student.last_name,
#                                student.first_name)
            else:
                addition['group'] = {'id': data.id}

        elif request.POST.get('cancel_button') is not None:
        # Press Cancel Button
            button += 1
            messages.warning(request, u"Редагування групи скасовано")
#            status_message = u"Додавання студента скасовано"
        
    else:
        try:
            addition['group'] = data
        except:
            messages.error(request, u"Оберіть існуючу групу для редагування")
            button = 1
    if button != 0:    
        return HttpResponseRedirect(reverse('groups'))#u"%s?status_message=%s" %
#               (reverse('home'), status_message))
    else:
        return render(request, 'students/groups_edit.html', 
            {'groups_all': groups_all, 'addition': addition, 'errors': errors })

# Delete Page

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    @property
    def success_url(self):
        return u"%s?status_message=Групу успішно видалено!" % reverse('groups')
  
def groups_delete(request, gid):
    groups = Group.objects.all()
    group = groups.get(pk=gid)
    if request.method == "POST":
        if request.POST.get('delete_button') is not None:
            try: 
                group.delete()
                message = u"=Групу успішно видалено"
            except:
                message = u"Виберіть коректну групу"
        elif request.POST.get('cancel_button') is not None:
            message = u"Видалення групи відмінено"
        return HttpResponseRedirect(
               u"%s?status_message=%s!" % (reverse('groups'), message))
    else:
        return render(request, 'students/groups_confirm_delete.html', 
            {'groups_all': groups, 'object': group})
  
