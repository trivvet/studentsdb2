# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from ..models.students import Student
from ..models.groups import Group
from ..models.journal import MonthJournal
from ..util import paginate, paginate_hand, get_current_group

# View for Journal

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'],
                '%Y-%m-%d').date()
            if month.year >= datetime.today().year and month.month > datetime.today().month:
                context['disabled'] = True
            elif month.year < datetime.today().year or month.month < datetime.today().month:
                context['current_day'] = 32
            else:
                context['current_day'] = datetime.today().day
        else:
            # othewise just display current month data
            today = datetime.utcnow()
            month = date(today.year, today.month, 1)
            context['current_day'] = datetime.today().day


        # calculate current, previous and next month dateils;
        # we need this for month navigarion element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        month_name = [u'Січень', u'Лютий', u'Березень', u'Квітень', u'Травень', u'Червень', u'Липень', u'Серпень', u'Вересень', u'Жовтень', u'Листопад', u'Грудень']
#        context['month_verbose'] = month.strftime('%B')
        context['month_verbose'] = month_name[month.month-1]

        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements

        day_name = [u'Пн', u'Вт', u'Ср', u'Чт', u'Пт', u'Сб', u'Нд']
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [
            {'day': d,
             'verbose': day_name[weekday(myear, mmonth, d)]}
            for d in range(1, number_of_days+1)]

        # get all students from database
        current_group = get_current_group(self.request)
        if current_group:
            queryset = Student.objects.filter(student_group=current_group)
        else:    
            if kwargs.get('pk'):
                queryset = Student.objects.filter(pk=kwargs['pk'])
            else:
                queryset = Student.objects.all().order_by('last_name')

        # це адреса для посту AJAX запиту, як бачите, ми
        # робитимемо його на цю ж в’юшку; в’юшка журналу
        # буде і показувати журнал і обслуговувати запити
        # типу пост на оновлення журналу
        update_url = reverse('journal')

        # застосовуємо пагінацію до списку студентів
        # handmade paginator
        context = paginate(queryset, 5, self.request, context, var_name='queryset')

        # пробігаємось по усіх студентах і збираємо необхідні дані
        context['students'] = []
        for student in context['queryset']:
            # try to get journal object by month selected
            try:
                journal = MonthJournal.objects.get(student_name=student, date=month)
            except Exception:
                journal = None

            # набиваємо дні для студента
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal,
                        'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })

            # набиваємо усі решту даних студента
            context['students'].append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        context['queryset'] = {}
        
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        # prepare student, dates and presense data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if current_date > datetime.today().date():
            return JsonResponse({'status': 'error', 'message': u'Заборонено змінювати статуси майбутніх відвідувань'})
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])
#        import pdb; pdb.set_trace()

        # get or create journal object for given student and month
        journal = MonthJournal.objects.get_or_create(student_name=student, date=month)[0]
        # set new presence on journal for given student and save result
        setattr(journal, 'present_day%s' % current_date.day, present)
        journal.save()

        i = 0
        while i < 10000000:
            i += 1
        # return success status
        return JsonResponse({'status': 'success'})
 
def journal_list(request):
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:    
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

        addition['counter'] = 3 * (addition['page'] - 1)
         
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
