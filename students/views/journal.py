from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from ..models.students import Student
from ..models.groups import Group
from ..models.journal import MonthJournal
from ..util import paginate, paginate_hand, get_current_group

# View for Journal

class JournalView(LoginRequiredMixin, TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'],
                '%Y-%m-%d').date()

            # check which days we need to disable
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
        # we need this for month navigation element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements

        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [
            {'day': d,
             'verbose': day_abbr[weekday(myear, mmonth, d)]}
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

        # this url for post AJAX request
        update_url = reverse('journal')

        # use pagination for student's list
        context = paginate(queryset, 5, self.request, context, var_name='queryset')

        # take needed elements for each students
        context['students'] = []
        for student in context['queryset']:
            # try to get journal object by month selected
            try:
                journal = MonthJournal.objects.get(student_name=student, date=month)
            except Exception:
                journal = None

            # add days for student
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal,
                        'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })

            # add all other data for student
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
            return JsonResponse({'status': 'error', 'message':
              _(u'Forbidden to change status future visits!')})
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # get or create journal object for given student and month
        journal = MonthJournal.objects.get_or_create(student_name=student, date=month)[0]
        
        # set new presence on journal for given student and save result
        setattr(journal, 'present_day%s' % current_date.day, present)
        journal.save()

        # return success status
        return JsonResponse({'status': 'success'})
