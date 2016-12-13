# -*- coding: utf-8 -*-

from datetime import datetime, date

from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView

from ..models.students import Student
from ..models.groups import Group

# View for Journal

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # перевіряємо чи передали на місяць в параметрі,
        # якщо ні - вичисляємо поточний;
        # поки що ми віддаємо лише поточний:

        today = datetime.today()
        month = date(today.year, today.month, 1)

        # Обчислюємо поточний рік, попередній і наступний місяці
        # а поки прибиваємо їх статично
        context['prev_month'] = '2016-10-01'
        context['next_month'] = '2016-12-01'
        context['year'] = '2016'

        # також поточний місяць;
        # змінну cur_month ми використовуватимемо пізніше
        # в пагінації; а month_verbose в
        # навігації помісячній
        context['cur_month'] = '2016-11-01'
        context['month_verbose'] = u"Листопад"

        # тут будемо обчислювати список днів у місяці,
        # а поки заб’ємо статично
        context['month_header'] = [
            {'day': 1, 'verbose': 'Пн'},
            {'day': 2, 'verbose': 'Вт'},
            {'day': 3, 'verbose': 'Ср'},
            {'day': 4, 'verbose': 'Чт'},
            {'day': 5, 'verbose': 'Пт'}]

        # витягуємо усіх студентів посортованих по Прізвищу
        queryset = Student.objects.order_by('last_name')

        # це адреса для посту AJAX запиту, як бачите, ми
        # робитимемо його на цю ж в’юшку; в’юшка журналу
        # буде і показувати журнал і обслуговувати запити
        # типу пост на оновлення журналу
        update_url = reverse('journal')

        # пробігаємось по усіх студентах і збираємо необхідні дані
        students = []
        for student in queryset:
            # TODO: витягуємо журнал для студента і вибраного місяця

            # набиваємо дні для студента
            days = []
            for day in range(1, 31):
                days.append({
                    'day': day,
                    'present': True,
                    'date': date(2016, 11, day).strftime('%Y-%m%d'),
                })

            # набиваємо усі решту даних студента
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        # застосовуємо пагінацію до списку студентів
        # handmade paginator
        if queryset.count() > 0:
            number = 5
            try:
                page = int(self.request.GET.get('page'))
            except:
                page = 1
            num_pages = queryset.count() / number
            if queryset.count() % number > 0:
                num_pages += 1
            # block for student_list template
            if num_pages > 0:
                page_range = []
                for i in range(1, num_pages+1):
                    page_range.append(i)
                context['addition'] = {
                    'has_other_pages': True,
                    'page_range': page_range}
        
            if page > 0 and page < num_pages:
                context['students'] = students[number*(page-1):number*page]
                context['addition']['page'] = page
            else:
                context['students'] = students[number*(num_pages-1):queryset.count()]
                context['addition']['page'] = num_pages
        else:
            context['addition'] = {}
        # end handmade paginator
        return context
 
def journal_list(request):
    students = Student.objects.all().order_by('id')

    # handmade paginator
    if students.count() > 0:
        number = 3
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        num_pages = students.count() / number
        if students.count() % number > 0:
            num_pages += 1
            # block for student_list template
        if num_pages > 0:
            page_range = []
            for i in range(1, num_pages+1):
                page_range.append(i)
            addition = {'has_other_pages': True, 'page_range': page_range}
        
        if page > 0 and page < num_pages:
            students = students[number*(page-1):number*page]
            addition['page'] = page
        else:
            students = students[number*(num_pages-1):students.count()]
            addition['page'] = num_pages
    else:
        addition = {}
    # end handmade paginator
    
    groups = Group.objects.all().order_by('title')
    days = []
    day_names = [u'Пн', u'Вт', u'Ср', u'Чт', u'Пт', u'Сб', u'Нд']
    for i in range(1, 31):
        days.append(day_names[i%7-1])
#   import pdb;pdb.set_trace()
    return render(request, 'students/journal.html', 
        {'students': students, 'groups_all': groups, 'days': days, 
         'day_names': day_names, 'addition': addition})


# Create your views here.
